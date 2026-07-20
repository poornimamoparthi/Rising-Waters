import os
import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

def main():
    print("--- 1. Loading Dataset ---")
    df = pd.read_csv('data/flood_data.csv')
    print(f"Dataset shape: {df.shape}")
    print("\nDescriptive Statistics:\n", df.describe(include='all'))

    os.makedirs('plots', exist_ok=True)
    os.makedirs('models', exist_ok=True)

    print("\n--- 2. Data Visualization & EDA ---")
    
    sns.set_theme(style="whitegrid")
    
    numerical_cols = ['Annual_Rainfall', 'Seasonal_Rainfall', 'Cloud_Visibility', 'Temperature', 'Humidity', 'Wind_Speed', 'Pressure']
    
    print("Generating distribution plots...")
    fig, axes = plt.subplots(3, 3, figsize=(15, 12))
    axes = axes.flatten()
    
    for i, col in enumerate(numerical_cols):
        sns.histplot(df[col].dropna(), kde=True, ax=axes[i], color='teal')
        axes[i].set_title(f'Distribution of {col}')
        
    if 'Weather_Condition' in df.columns:
        sns.countplot(x='Weather_Condition', data=df, ax=axes[7], hue='Weather_Condition', palette='Set2', legend=False)
        axes[7].set_title('Distribution of Weather_Condition')
    
    sns.countplot(x='Flood_Chance', data=df, ax=axes[8], hue='Flood_Chance', palette='coolwarm', legend=False)
    axes[8].set_title('Distribution of Flood_Chance')
    
    plt.tight_layout()
    plt.savefig('plots/distribution_plots.png', dpi=300)
    plt.close()
    
    print("Generating box plots for outlier visualization...")
    fig, axes = plt.subplots(3, 3, figsize=(15, 12))
    axes = axes.flatten()
    for i, col in enumerate(numerical_cols):
        sns.boxplot(y=df[col], ax=axes[i], color='lightblue')
        axes[i].set_title(f'Box plot of {col}')
    
    for j in range(len(numerical_cols), len(axes)):
        fig.delaxes(axes[j])
        
    plt.tight_layout()
    plt.savefig('plots/box_plots.png', dpi=300)
    plt.close()

    print("Generating correlation heatmap...")
    plt.figure(figsize=(12, 10))
    temp_df = df.copy()
    for col in ['Cloud_Visibility', 'Temperature']:
        temp_df[col] = temp_df[col].fillna(temp_df[col].median())
    
    if 'Weather_Condition' in temp_df.columns:
        temp_df = pd.get_dummies(temp_df, columns=['Weather_Condition'], prefix='Weather', prefix_sep='_')
        for col in temp_df.columns:
            if col.startswith('Weather_'):
                temp_df[col] = temp_df[col].astype(int)
    
    correlation_matrix = temp_df.corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
    plt.title('Correlation Matrix Heatmap')
    plt.tight_layout()
    plt.savefig('plots/correlation_heatmap.png', dpi=300)
    plt.close()

    print("\n--- 3. Data Preprocessing ---")
    
    print("Handling missing values (Imputing with median/mode)...")
    missing_before = df.isnull().sum()
    print("Missing values before imputation:\n", missing_before[missing_before > 0])
    
    for col in ['Cloud_Visibility', 'Temperature']:
        median_val = df[col].median()
        df[col] = df[col].fillna(median_val)
        
    if 'Weather_Condition' in df.columns:
        mode_val = df['Weather_Condition'].mode()[0]
        df['Weather_Condition'] = df['Weather_Condition'].fillna(mode_val)
        
    print("Missing values after imputation:\n", df.isnull().sum())

    print("Treating outliers by capping at 1.5 * IQR limits...")
    for col in numerical_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers_lower = (df[col] < lower_bound).sum()
        outliers_upper = (df[col] > upper_bound).sum()
        if outliers_lower > 0 or outliers_upper > 0:
            print(f"Column '{col}': capping {outliers_lower} lower and {outliers_upper} upper outliers.")
            
        df[col] = np.clip(df[col], lower_bound, upper_bound)

    print("Encoding categorical variables...")
    df_encoded = pd.get_dummies(df, columns=['Weather_Condition'], prefix='Weather', prefix_sep='_')
    
    for col in df_encoded.columns:
        if col.startswith('Weather_'):
            df_encoded[col] = df_encoded[col].astype(int)

    X_features = [col for col in df_encoded.columns if col != 'Flood_Chance']
    print(f"Encoded features list: {X_features}")

    X = df_encoded[X_features]
    y = df_encoded['Flood_Chance']
    
    print("Scaling independent variables using StandardScaler...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_scaled_df = pd.DataFrame(X_scaled, columns=X_features)
    
    print("Splitting dataset into train (80%) and test (20%) sets...")
    X_train, X_test, y_train, y_test = train_test_split(X_scaled_df, y, test_size=0.2, random_state=42, stratify=y)
    print(f"Training shape: {X_train.shape}, Test shape: {X_test.shape}")

    print("\n--- 4. Model Building & Evaluation ---")
    
    models = {
        'Decision Tree': DecisionTreeClassifier(random_state=42, max_depth=6),
        'Random Forest': RandomForestClassifier(random_state=42, n_estimators=100, max_depth=8),
        'K-Nearest Neighbors': KNeighborsClassifier(n_neighbors=7),
        'XGBoost': XGBClassifier(random_state=42, n_estimators=150, learning_rate=0.05, max_depth=5, eval_metric='logloss')
    }
    
    best_model_name = None
    best_accuracy = 0.0
    best_model = None
    
    for name, model in models.items():
        print(f"\nTraining {name}...")
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        acc = accuracy_score(y_test, y_pred)
        print(f"Accuracy Score: {acc:.4f}")
        print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
        print("Classification Report:\n", classification_report(y_test, y_pred))
        
        if acc > best_accuracy:
            best_accuracy = acc
            best_model_name = name
            best_model = model

    print(f"\nBest Model: {best_model_name} with Accuracy: {best_accuracy:.4f}")
    
    xgb_model = models['XGBoost']
    xgb_test_acc = accuracy_score(y_test, xgb_model.predict(X_test))
    print(f"Saving XGBoost model (Accuracy: {xgb_test_acc:.4f}) and StandardScaler to 'floods.save'...")
    
    save_data = {
        'model': xgb_model,
        'scaler': scaler,
        'features': X_features
    }
    
    joblib.dump(save_data, 'floods.save')
    print("Saved successfully to floods.save!")

if __name__ == '__main__':
    main()
