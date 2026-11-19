"""Project 13: DataCo - audit, EDA, baseline ML (không rò rỉ thông tin hậu giao hàng).
Chạy: python project13_pipeline.py --input '7_PJ13_2521001054_Nguyễn Lê Nhật Hạ.csv'
Cài: pip install pandas numpy matplotlib scikit-learn pyarrow
"""
import sys
import argparse
from pathlib import Path

# Cấu hình UTF-8 cho console Windows
if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (classification_report, roc_auc_score, average_precision_score,
                             ConfusionMatrixDisplay, precision_recall_curve)

PII = ['Customer Email','Customer Password','Customer Fname','Customer Lname',
       'Customer Street','Latitude','Longitude','Product Image']
NUMERIC = ['Days for shipping (real)','Days for shipment (scheduled)',
           'Sales','Sales per customer','Benefit per order','Order Item Discount',
           'Order Item Discount Rate','Order Item Quantity','Order Item Product Price',
           'Order Item Total','Order Item Profit Ratio','Order Profit Per Order','Product Price']
MISSING = {'?','-','none','nan','null','n/a',''}
FEATURES = ['Shipping Mode','Market','Order Region','Customer Segment',
            'Category Name','Department Name','Order Item Quantity',
            'Order Item Product Price','Order Item Discount Rate',
            'order_month','order_weekday']

def clean_numeric(s, percent=False):
    x=s.astype('string').str.strip()
    x=x.mask(x.str.lower().isin(MISSING))
    # Chỉ cho phép đơn vị tiền tệ trong cột tiền, % trong cột tỷ lệ.
    suffix = r'\s*(?:USD|VND|đ)\s*$' if not percent else r'\s*%\s*$'
    x=x.str.replace(suffix,'',regex=True,case=False)
    # Không xóa tùy tiện kg hay các chữ còn lại: ép số lỗi thành NaN.
    x=x.str.replace(r'^(-?\d{1,3}(?:,\d{3})+)(\.\d+)?$',
                    lambda m:m.group(1).replace(',','')+(m.group(2) or ''),regex=True)
    return pd.to_numeric(x,errors='coerce')

def main(path,out):
    out.mkdir(parents=True,exist_ok=True)
    df=pd.read_csv(path,encoding='utf-8-sig',low_memory=False,dtype='string')
    if not {'Late_delivery_risk','Order Id','Order Item Id','Shipping Mode'}.issubset(df.columns):
        raise ValueError('Thiếu cột bắt buộc trong schema DataCo')
    if len(df.columns)!=53: print('CẢNH BÁO: file không có 53 cột:',len(df.columns))
    original_rows=len(df)
    df=df.drop(columns=[c for c in PII if c in df],errors='ignore')
    df=df.replace(r'^\s*$',pd.NA,regex=True)
    # Loại bản ghi trùng hoàn toàn; không loại trùng chỉ theo Order Id.
    dup=int(df.duplicated().sum());df=df.drop_duplicates().copy()
    for c in NUMERIC:
        if c in df:
            df[c]=clean_numeric(df[c],percent=c in ['Order Item Discount Rate','Order Item Profit Ratio'])
    # Giữ nguyên nhãn gốc, không ghi đè nếu chưa có xác nhận nghiệp vụ.
    raw_label=clean_numeric(df['Late_delivery_risk'])
    raw_label=raw_label.where(raw_label.isin([0,1]))
    a,b=df['Days for shipping (real)'],df['Days for shipment (scheduled)']
    valid=a.notna() & b.notna() & a.ge(0) & b.ge(0)
    derived=pd.Series(pd.NA,index=df.index,dtype='Int8')
    derived.loc[valid]=(a[valid]>b[valid]).astype('int8')
    conflict=int((raw_label.notna() & derived.notna() & raw_label.ne(derived)).fillna(False).sum())
    df['Late_delivery_risk']=raw_label.astype('Int8')
    df['order date (DateOrders)']=pd.to_datetime(df['order date (DateOrders)'],errors='coerce')
    df['shipping date (DateOrders)']=pd.to_datetime(df['shipping date (DateOrders)'],errors='coerce')
    bad_dates=int((df['shipping date (DateOrders)']<df['order date (DateOrders)']).sum())
    # Đánh dấu bất thường; không sửa bằng abs() hoặc xóa tự động.
    rules={
      'Order Item Quantity': lambda x:x<=0,
      'Order Item Discount Rate':lambda x:(x<0)|(x>1),
      'Product Price':lambda x:x<0,
      'Days for shipping (real)':lambda x:x<0,
      'Days for shipment (scheduled)':lambda x:x<0,
    }
    violations={c:int(fn(df[c]).sum()) for c,fn in rules.items() if c in df}
    for c in df.select_dtypes(include=['string']).columns:
        df[c]=df[c].str.strip()
        if c not in ['Order Id','Order Item Id','Customer Id','Order Customer Id','Product Card Id']:
            df[c]=df[c].fillna('Unknown')
        if df[c].nunique(dropna=True)<200:
            df[c]=df[c].astype('category')
    # Báo cáo không chứa thông tin định danh hay giá trị bản ghi.
    quality=pd.DataFrame({'column':df.columns,'dtype':df.dtypes.astype(str).values,
      'null_count':df.isna().sum().values,'null_pct':(df.isna().mean()*100).values,
      'unknown_count':[int(df[c].astype('string').eq('Unknown').sum()) if
        (pd.api.types.is_string_dtype(df[c]) or isinstance(df[c].dtype,pd.CategoricalDtype)) else 0 for c in df.columns]})
    quality.to_csv(out/'DataCo_Data_Quality_Report.csv',index=False)
    summary=pd.DataFrame({'metric':['original_rows','rows_after_dedup','exact_duplicates_removed',
      'label_conflicts','invalid_date_order']+list(violations),
      'value':[original_rows,len(df),dup,conflict,bad_dates]+list(violations.values())})
    summary.to_csv(out/'DataCo_Audit_Summary.csv',index=False)
    # Dữ liệu phân tích; PII đã bị xóa, nhưng vẫn cần hạn chế chia sẻ vì có thể có định danh khác.
    df.to_csv(out/'DataCo_Cleaned_Full.csv',index=False)
    print(f"-> Đã xuất tệp dữ liệu sạch: {out / 'DataCo_Cleaned_Full.csv'}")

    # =========================================================================
    # BASELINE ML PIPELINE (Không rò rỉ thông tin hậu giao hàng)
    # =========================================================================
    print("\n--- BẮT ĐẦU HUẤN LUYỆN BASELINE MACHINE LEARNING ---")
    # Trích xuất đặc trưng thời gian
    df['order_month'] = df['order date (DateOrders)'].dt.month.fillna(-1).astype(int).astype(str)
    df['order_weekday'] = df['order date (DateOrders)'].dt.weekday.fillna(-1).astype(int).astype(str)

    # Lọc các dòng có nhãn mục tiêu hợp lệ
    ml_df = df[df['Late_delivery_risk'].notna()].copy()

    num_cols = [
        'Order Item Quantity',
        'Order Item Product Price',
        'Order Item Discount Rate'
    ]
    cat_cols = [c for c in FEATURES if c not in num_cols]

    # Chuẩn hóa kiểu dữ liệu đồng nhất
    for c in num_cols:
        ml_df[c] = pd.to_numeric(ml_df[c], errors='coerce')
    for c in cat_cols:
        ml_df[c] = ml_df[c].fillna('Unknown').astype(str)

    X = ml_df[FEATURES]
    y = ml_df['Late_delivery_risk'].astype(int)

    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"-> Quy mô tập Train: {len(X_train):,} dòng | Tập Test: {len(X_test):,} dòng")

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', Pipeline([
                ('imputer', SimpleImputer(strategy='median')),
                ('scaler', StandardScaler())
            ]), num_cols),
            ('cat', Pipeline([
                ('imputer', SimpleImputer(strategy='constant', fill_value='Unknown')),
                ('onehot', OneHotEncoder(handle_unknown='ignore'))
            ]), cat_cols)
        ]
    )

    models = {
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
    }

    ml_metrics = []
    for name, clf in models.items():
        print(f"\n[Huấn luyện {name}]...")
        pipe = Pipeline([
            ('preprocessor', preprocessor),
            ('classifier', clf)
        ])
        pipe.fit(X_train, y_train)
        y_pred = pipe.predict(X_test)
        y_prob = pipe.predict_proba(X_test)[:, 1]

        auc = roc_auc_score(y_test, y_prob)
        ap = average_precision_score(y_test, y_prob)
        print(f"-> {name} | ROC-AUC: {auc:.4f} | PR-AUC: {ap:.4f}")
        report = classification_report(y_test, y_pred, output_dict=True)
        ml_metrics.append({
            'Model': name,
            'ROC_AUC': round(auc, 4),
            'PR_AUC': round(ap, 4),
            'Accuracy': round(report['accuracy'], 4),
            'Precision': round(report['1']['precision'], 4),
            'Recall': round(report['1']['recall'], 4),
            'F1-Score': round(report['1']['f1-score'], 4)
        })

    ml_summary_df = pd.DataFrame(ml_metrics)
    ml_summary_df.to_csv(out / 'DataCo_Baseline_ML_Evaluation.csv', index=False)
    print(f"\n-> Đã lưu bảng đánh giá ML: {out / 'DataCo_Baseline_ML_Evaluation.csv'}")
    print(ml_summary_df.to_string(index=False))
    print("\n=== HOÀN TẤT TOÀN BỘ PIPELINE THÀNH CÔNG ===")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="DataCo Pipeline PRJ-13: Audit, Clean & Baseline ML")
    parser.add_argument('--input', type=str, default='7_PJ13_2521001054_Nguyễn Lê Nhật Hạ.csv', help='File CSV đầu vào')
    parser.add_argument('--out', type=str, default='output', help='Thư mục lưu kết quả đầu ra')
    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.out)
    main(input_path, output_dir)