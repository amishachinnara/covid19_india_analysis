import os
import math
import json
import time
import random
import argparse
from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader

try:
    import networkx as nx
    _HAS_NX = True
except Exception:
    _HAS_NX = False

SEED = 42
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#1
def load_and_align(covid_csv: str, mobility_csv: str,
                   date_col: str = "date", region_col: str = "region_id",
                   target_col: str = "cases") -> Tuple[pd.DataFrame, List[str], List[pd.Timestamp]]:
    

    if not os.path.exists(covid_csv):
        raise FileNotFoundError(f"covid_csv not found: {covid_csv}")
    if not os.path.exists(mobility_csv):
        raise FileNotFoundError(f"mobility_csv not found: {mobility_csv}")

    covid = pd.read_csv(r"/Users/anushree/Anu/Desktop/Project/covid-19_india_cases.csv")
    mob = pd.read_csv(r"/Users/anushree/Anu/Desktop/Project/covid-19_india_mobility.csv")

    covid[date_col] = pd.to_datetime(covid[date_col])
    mob[date_col] = pd.to_datetime(mob[date_col])

    covid[region_col] = covid[region_col].astype(str)
    mob[region_col] = mob[region_col].astype(str)

    if target_col not in covid.columns:
        raise ValueError(f"Target column '{target_col}' not found in covid_csv")

    panel = pd.merge(covid, mob, on=[date_col, region_col], how="left", suffixes=("", "_m"))
    panel.sort_values([date_col, region_col], inplace=True)
    regions = sorted(panel[region_col].unique().tolist())
    dates = sorted(panel[date_col].unique().tolist())

    panel = (
        panel.set_index([date_col, region_col])
             .groupby(level=region_col)
             .apply(lambda df: df.ffill().bfill())
    )
    panel.index = panel.index.droplevel(0)
    panel = panel.reset_index()

    return panel, regions, dates

import os
import pandas as pd
from typing import Tuple, List

def load_and_align(covid_csv: str, mobility_csv: str,
                   date_col: str = "date", region_col: str = "region_id",
                   target_col: str = "cases") -> Tuple[pd.DataFrame, List[str], List[pd.Timestamp]]:
    
    if not os.path.exists(covid_csv):
        raise FileNotFoundError(f"covid_csv not found: {covid_csv}\nCurrent dir: {os.getcwd()}")
    if not os.path.exists(mobility_csv):
        raise FileNotFoundError(f"mobility_csv not found: {mobility_csv}\nCurrent dir: {os.getcwd()}")

    covid = pd.read_csv(covid_csv)
    mob = pd.read_csv(mobility_csv)


    covid[date_col] = pd.to_datetime(covid[date_col])
    mob[date_col] = pd.to_datetime(mob[date_col])
    
    covid[region_col] = covid[region_col].astype(str)
    mob[region_col] = mob[region_col].astype(str)

    if target_col not in covid.columns:
        raise ValueError(f"Target column '{target_col}' not found in covid_csv")

  
    panel = pd.merge(covid, mob, on=[date_col, region_col], how="left", suffixes=("", "_m"))

  
    panel.sort_values([date_col, region_col], inplace=True)

    
    regions = sorted(panel[region_col].unique().tolist())
    dates = sorted(panel[date_col].unique().tolist())

    
    panel = (
        panel.set_index([date_col, region_col])
             .groupby(level=region_col)
             .apply(lambda df: df.ffill().bfill())
    )

   
    panel.index = panel.index.droplevel(0)
    panel = panel.reset_index()

    return panel, regions, dates

covid_csv = "covid-19_india_cases.csv"
mobility_csv = "covid-19_india_mobility.csv"


if not os.path.exists(covid_csv) or not os.path.exists(mobility_csv):
    print(" CSVs not found in:", os.getcwd())
    print("Creating dummy CSVs for testing...\n")

    covid_data = {
        "date": pd.date_range("2020-01-01", periods=5),
        "region_id": [1, 1, 1, 2, 2],
        "cases": [10, 12, 15, 5, 7],
        "recovered": [1, 2, 3, 0, 1],
        "death": [0, 0, 1, 0, 0],
    }
    mobility_data = {
        "date": pd.date_range("2020-01-01", periods=5),
        "region_id": [1, 1, 1, 2, 2],
        "retail": [100, 98, 95, 110, 108],
        "transit": [80, 78, 75, 85, 83],
        "workplace": [70, 72, 74, 65, 63],
    }

    pd.DataFrame(covid_data).to_csv(covid_csv, index=False)
    pd.DataFrame(mobility_data).to_csv(mobility_csv, index=False)


panel, regions, dates = load_and_align(covid_csv, mobility_csv)

print(" Data merged successfully!")
print("Regions:", regions)
print("Dates:", dates[:5], "...")  
print(panel.head())

import os
import pandas as pd
from typing import Tuple, List

def load_and_align(covid_csv: str, mobility_csv: str,
                   date_col: str = "date", region_col: str = "region_id",
                   target_col: str = "cases") -> Tuple[pd.DataFrame, List[str], List[pd.Timestamp]]:
    
    if not os.path.exists(covid_csv):
        raise FileNotFoundError(f"covid_csv not found: {covid_csv}")
    if not os.path.exists(mobility_csv):
        raise FileNotFoundError(f"mobility_csv not found: {mobility_csv}")

    
    covid = pd.read_csv(covid_csv)
    mob = pd.read_csv(mobility_csv)

    covid[date_col] = pd.to_datetime(covid[date_col])
    mob[date_col] = pd.to_datetime(mob[date_col])


    covid[region_col] = covid[region_col].astype(str)
    mob[region_col] = mob[region_col].astype(str)

    
    if target_col not in covid.columns:
        raise ValueError(f"Target column '{target_col}' not found in covid_csv")


    panel = pd.merge(covid, mob, on=[date_col, region_col], how="left", suffixes=("", "_m"))


    panel.sort_values([date_col, region_col], inplace=True)

    
    regions = sorted(panel[region_col].unique().tolist())
    dates = sorted(panel[date_col].unique().tolist())

    
    panel = (
        panel.set_index([date_col, region_col])
             .groupby(level=region_col)
             .apply(lambda df: df.ffill().bfill())
    )

    
    panel.index = panel.index.droplevel(0)
    panel = panel.reset_index()

    return panel, regions, dates


if __name__ == "_main_":
    covid_csv = r"C:\Users\sudha\OneDrive\Desktop\Project\covid.csv"
    mobility_csv = r"C:\Users\sudha\OneDrive\Desktop\Project\mobility.csv"

    try:
        panel, regions, dates = load_and_align(covid_csv, mobility_csv)

        print(" Data merged successfully!")
        print("Regions:", regions[:5], "... total:", len(regions))
        print("Dates:", dates[:5], "... total:", len(dates))
        print("Merged panel shape:", panel.shape)
        print(panel.head())

    except Exception as e:
        print(" Error:", e)
# =============================
# 2) PREPROCESS & SCALE
# =============================
@dataclass
class PreprocessConfig:
    feature_cols: List[str]
    target_col: str = "cases"
    scaler_type: str = "standard"  # "standard" or "minmax"
    clip_cases_at: Optional[float] = None  # e.g., 99 to clip at 99th percentile


def preprocess_panel(panel: pd.DataFrame, regions: List[str], dates: List[pd.Timestamp],
                      cfg: PreprocessConfig) -> Tuple[np.ndarray, np.ndarray, Dict]:
    """Build tensors X:[T,N,F], y:[T,N] from panel table (unscaled)."""
    for c in cfg.feature_cols + [cfg.target_col]:
        if c not in panel.columns:
            raise ValueError(f"Column '{c}' not found in merged panel")

    df = panel.copy()
    if cfg.clip_cases_at is not None:
        thresh = np.percentile(df[cfg.target_col].dropna().values, cfg.clip_cases_at)
        df[cfg.target_col] = df[cfg.target_col].clip(upper=thresh)

    T = len(dates)
    N = len(regions)
    Ff = len(cfg.feature_cols)

    date_to_idx = {d: i for i, d in enumerate(dates)}
    region_to_idx = {r: i for i, r in enumerate(regions)}

    X = np.zeros((T, N, Ff), dtype=np.float32)
    y = np.zeros((T, N), dtype=np.float32)

    for _, row in df.iterrows():
        t = date_to_idx[row['date']]
        n = region_to_idx[row['region_id']]
        X[t, n, :] = row[cfg.feature_cols].to_numpy(dtype=np.float32)
        y[t, n] = float(row[cfg.target_col])

    X = np.nan_to_num(X)
    y = np.nan_to_num(y)

    meta = {
        'regions': regions,
        'dates': [pd.Timestamp(d) for d in dates],
        'feature_cols': cfg.feature_cols,
        'target_col': cfg.target_col,
    }
    return X, y, meta


class Standardizer:
    """Fits on TRAIN split only; transforms X (features) and y (target)."""
    def _init_(self, mode: str = "standard"):
        self.mode = mode
        self.scaler_x = StandardScaler() if mode == "standard" else MinMaxScaler()
        self.scaler_y = StandardScaler() if mode == "standard" else MinMaxScaler()
        self._fitted = False

    def fit(self, X_train: np.ndarray, y_train: np.ndarray):
        T, N, F = X_train.shape
        self.scaler_x.fit(X_train.reshape(T*N, F))
        self.scaler_y.fit(y_train.reshape(-1, 1))
        self._fitted = True

    def transform(self, X: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        assert self._fitted, "Standardizer not fitted"
        T, N, F = X.shape
        Xs = self.scaler_x.transform(X.reshape(T*N, F)).reshape(T, N, F)
        ys = self.scaler_y.transform(y.reshape(-1, 1)).reshape(T, N)
        return Xs.astype(np.float32), ys.astype(np.float32)

    def inverse_y(self, y_scaled: np.ndarray) -> np.ndarray:
        return self.scaler_y.inverse_transform(y_scaled.reshape(-1, 1)).reshape(y_scaled.shape)
        
# 3==== FULL WORKING EXAMPLE ====
import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Dict, Any

# ==== CONFIG CLASS ====
@dataclass
class PreprocessConfig:
    feature_cols: List[str]
    target_col: str

# ==== PREPROCESS FUNCTION ====
def preprocess_panel(
    panel: pd.DataFrame,
    regions: List[str],
    dates: List[pd.Timestamp],
    cfg: PreprocessConfig
) -> Tuple[np.ndarray, np.ndarray, Dict[str, Any]]:
    """
    Converts panel data into X (features), y (targets), and meta info
    aligned by regions x dates.
    """
    X_list, y_list = [], []
    for d in dates:
        for r in regions:
            row = panel[(panel["date"] == d) & (panel["region_id"] == r)]
            if not row.empty:
                X_list.append(row[cfg.feature_cols].values[0])
                y_list.append(row[cfg.target_col].values[0])
            else:
                # handle missing with NaN
                X_list.append([np.nan] * len(cfg.feature_cols))
                y_list.append(np.nan)
    X = np.array(X_list, dtype=float)
    y = np.array(y_list, dtype=float).reshape(-1, 1)
    meta = {"regions": regions, "dates": dates}
    return X, y, meta

# ==== STANDARDIZER CLASS ====
class Standardizer:
    def __init__(self, mode: str = "standard"):
        self.mode = mode

    def fit(self, X: np.ndarray, y: np.ndarray):
        if self.mode == "standard":
            self.x_mean = X.mean(axis=0)
            self.x_std = X.std(axis=0)
            self.y_mean = y.mean()
            self.y_std = y.std()
        else:
            raise ValueError("Only 'standard' mode implemented here.")

    def transform(self, X: np.ndarray, y: np.ndarray):
        Xs = (X - self.x_mean) / (self.x_std + 1e-8)
        ys = (y - self.y_mean) / (self.y_std + 1e-8)
        return Xs, ys

    def inverse_y(self, ys: np.ndarray):
        return ys * (self.y_std + 1e-8) + self.y_mean

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# ==== Dummy dataframe ====
panel = pd.DataFrame({
    "date": [pd.Timestamp("2020-01-01"), pd.Timestamp("2020-01-01"),
             pd.Timestamp("2020-01-02"), pd.Timestamp("2020-01-02")],
    "region_id": ["A", "B", "A", "B"],
    "feat1": [0.5, 0.7, 0.6, 0.8],
    "feat2": [0.2, 0.4, 0.3, 0.5],
    "cases": [10, 20, 15, 25],
})

regions = ["A", "B"]
dates = [pd.Timestamp("2020-01-01"), pd.Timestamp("2020-01-02")]

# ==== PreprocessConfig ====
class PreprocessConfig:
    def __init__(self, feature_cols, target_col):
        self.feature_cols = feature_cols
        self.target_col = target_col

# ==== Simple preprocess function ====
def preprocess_panel(panel, regions, dates, cfg):
    df = panel[panel["region_id"].isin(regions) & panel["date"].isin(dates)]
    X = df[cfg.feature_cols].to_numpy(dtype=float)
    y = df[[cfg.target_col]].to_numpy(dtype=float)   # keep as 2D
    meta = df[["date", "region_id"]]
    return X, y, meta

# ==== Standardizer ====
class Standardizer:
    def __init__(self, mode="standard"):
        if mode == "standard":
            self.x_scaler = StandardScaler()
            self.y_scaler = StandardScaler()
        elif mode == "minmax":
            self.x_scaler = MinMaxScaler()
            self.y_scaler = MinMaxScaler()
        else:
            raise ValueError("mode must be 'standard' or 'minmax'")
    
    def fit(self, X, y):
        self.x_scaler.fit(X)
        self.y_scaler.fit(y)
    
    def transform(self, X, y):
        Xs = self.x_scaler.transform(X)
        ys = self.y_scaler.transform(y)
        return Xs, ys
    
    def inverse_y(self, ys):
        return self.y_scaler.inverse_transform(ys)

# ==== TEST PIPELINE ====
cfg = PreprocessConfig(feature_cols=["feat1", "feat2"], target_col="cases")
X, y, meta = preprocess_panel(panel, regions, dates, cfg)

print("Raw X shape:", X.shape)
print("Raw y shape:", y.shape)
print("X:\n", X)
print("y:\n", y)

scaler = Standardizer(mode="standard")
scaler.fit(X, y)
Xs, ys = scaler.transform(X, y)

print("\nScaled X:\n", Xs)
print("\nScaled y:\n", ys)

y_inv = scaler.inverse_y(ys)
print("\nInverse y:\n", y_inv)

import math
import numpy as np
import torch
from torch.utils.data import Dataset
from dataclasses import dataclass


# ----------------------------
# 4Split Configuration
# ----------------------------
@dataclass
class SplitConfig:
    seq_len: int = 14      # input sequence length
    horizon: int = 7       # prediction horizon
    val_ratio: float = 0.1
    test_ratio: float = 0.1


# ----------------------------
# Sliding Window Maker
# ----------------------------
def make_windows(X: np.ndarray, y: np.ndarray, cfg: SplitConfig):
    """
    Create temporal sliding windows for seq2seq forecasting.

    Args:
        X: [T, N, F]  (time, regions, features)
        y: [T, N]     (time, regions)
        cfg: SplitConfig

    Returns:
        train, val, test splits of (Xw, yw)
          - Xw: [M, S, N, F]
          - yw: [M, H, N]
    """
    T, N, F = X.shape
    S = cfg.seq_len
    H = cfg.horizon
    max_start = T - (S + H)
    if max_start <= 0:
        raise ValueError("Not enough time steps for the given seq_len and horizon")

    X_list, y_list = [], []
    for t0 in range(max_start + 1):
        X_list.append(X[t0:t0+S])
        y_list.append(y[t0+S:t0+S+H])
    Xw = np.stack(X_list, axis=0).astype(np.float32)  # [M, S, N, F]
    yw = np.stack(y_list, axis=0).astype(np.float32)  # [M, H, N]

    # Split
    M = Xw.shape[0]
    n_test = int(math.floor(cfg.test_ratio * M))
    n_val = int(math.floor(cfg.val_ratio * (M - n_test)))
    n_train = M - n_val - n_test

    idx_train = slice(0, n_train)
    idx_val = slice(n_train, n_train + n_val)
    idx_test = slice(n_train + n_val, M)

    return (Xw[idx_train], yw[idx_train]), (Xw[idx_val], yw[idx_val]), (Xw[idx_test], yw[idx_test])


# ----------------------------
# PyTorch Dataset
# ----------------------------
class STWindowDataset(Dataset):
    def __init__(self, Xw: np.ndarray, yw: np.ndarray):
        self.Xw = torch.from_numpy(Xw)  # convert to torch.Tensor
        self.yw = torch.from_numpy(yw)

    def _len_(self):
        return self.Xw.shape[0]

    def _getitem_(self, idx):
        return self.Xw[idx], self.yw[idx]


# ----------------------------
# DEMO RUN
# ----------------------------
if __name__ == "__main_-":
    np.random.seed(0)

    # Fake data [T=30 days, N=3 regions, F=2 mobility features]
    X = np.random.rand(30, 3, 2).astype(np.float32)
    y = np.random.rand(30, 3).astype(np.float32) * 100  # cases

    cfg = SplitConfig(seq_len=5, horizon=3, val_ratio=0.2, test_ratio=0.2)

    (Xtr, ytr), (Xval, yval), (Xte, yte) = make_windows(X, y, cfg)

    print("Train X shape:", Xtr.shape)
    print("Train y shape:", ytr.shape)
    print("Val X shape:", Xval.shape)
    print("Val y shape:", yval.shape)
    print("Test X shape:", Xte.shape)
    print("Test y shape:", yte.shape)

    # Dataset test
    train_ds = STWindowDataset(Xtr, ytr)
    print("\nOne sample X shape:", train_ds[0][0].shape)  # (seq_len, N, F)
    print("One sample y shape:", train_ds[0][1].shape)    # (horizon, N)
    
import torch
import torch.nn as nn
import torch.nn.functional as F

# -----------------------------
# 5Graph Convolution Layer
# -----------------------------
class GCNLayer(nn.Module):
    def __init__(self, in_feats: int, out_feats: int, bias: bool = True):
        super().__init__()
        self.lin = nn.Linear(in_feats, out_feats, bias=bias)

    def forward(self, X: torch.Tensor, A_hat: torch.Tensor) -> torch.Tensor:
        # X: [N, F_in], A_hat: [N, N]
        return A_hat @ self.lin(X)


# -----------------------------
# Two-layer Spatial GCN
# -----------------------------
class SpatialGCN(nn.Module):
    def __init__(self, in_feats: int, hidden: int, out_feats: int, dropout: float = 0.1):
        super().__init__()
        self.gcn1 = GCNLayer(in_feats, hidden)
        self.gcn2 = GCNLayer(hidden, out_feats)
        self.dropout = nn.Dropout(dropout)

    def forward(self, X: torch.Tensor, A_hat: torch.Tensor) -> torch.Tensor:
        # X: [N, F_in]
        H = F.relu(self.gcn1(X, A_hat))
        H = self.dropout(H)
        H = self.gcn2(H, A_hat)
        return F.relu(H)  # [N, out_feats]


# -----------------------------
# Full STGNN: Spatial + Temporal
# -----------------------------
class STGNN(nn.Module):
    def __init__(self, num_nodes: int, in_feats: int,
                 gcn_hidden: int = 32, gcn_out: int = 32,
                 rnn_hidden: int = 64, horizon: int = 7, dropout: float = 0.1):
        super().__init__()
        self.num_nodes = num_nodes
        self.horizon = horizon
        self.spatial = SpatialGCN(in_feats, gcn_hidden, gcn_out, dropout)
        self.rnn = nn.GRU(input_size=gcn_out, hidden_size=rnn_hidden, batch_first=True)
        self.head = nn.Linear(rnn_hidden, horizon)  # output per node
        self.dropout = nn.Dropout(dropout)

    def forward(self, X_seq: torch.Tensor, A_hat: torch.Tensor) -> torch.Tensor:
        """
        X_seq: [B, S, N, F]
        A_hat: [N, N]
        Returns: y_hat [B, H, N]
        """
        B, S, N, F_in = X_seq.shape
        assert N == self.num_nodes

        # Spatial GCN at each timestep
        gcn_outs = []
        for t in range(S):
            Xt = X_seq[:, t]  # [B, N, F]
            Gt = []
            for b in range(B):
                Hb = self.spatial(Xt[b], A_hat)  # [N, gcn_out]
                Gt.append(Hb.unsqueeze(0))
            Gt = torch.cat(Gt, dim=0)  # [B, N, gcn_out]
            gcn_outs.append(Gt.unsqueeze(1))
        G = torch.cat(gcn_outs, dim=1)  # [B, S, N, gcn_out]

        # Temporal GRU per node
        BN = B * N
        G_reshaped = G.reshape(BN, S, -1)          # [B*N, S, gcn_out]
        _, h_last = self.rnn(G_reshaped)           # h_last: [1, B*N, rnn_hidden]
        HN = h_last.squeeze(0)                     # [B*N, rnn_hidden]
        HN = self.dropout(HN)
        YN = self.head(HN)                         # [B*N, horizon]

        # Reshape back to [B, H, N]
        Y = YN.reshape(B, N, self.horizon).permute(0, 2, 1).contiguous()
        return Y
import torch
import torch.nn as nn
import torch.nn.functional as F

# -----------------------------
# 6Graph Convolution Layer
# -----------------------------
class GCNLayer(nn.Module):
    def __init__(self, in_feats: int, out_feats: int, bias: bool = True):
        super().__init__()
        self.lin = nn.Linear(in_feats, out_feats, bias=bias)

    def forward(self, X: torch.Tensor, A_hat: torch.Tensor) -> torch.Tensor:
        # X: [N, F_in], A_hat: [N, N]
        return A_hat @ self.lin(X)


# -----------------------------
# Two-layer Spatial GCN
# -----------------------------
class SpatialGCN(nn.Module):
    def __init__(self, in_feats: int, hidden: int, out_feats: int, dropout: float = 0.1):
        super().__init__()
        self.gcn1 = GCNLayer(in_feats, hidden)
        self.gcn2 = GCNLayer(hidden, out_feats)
        self.dropout = nn.Dropout(dropout)

    def forward(self, X: torch.Tensor, A_hat: torch.Tensor) -> torch.Tensor:
        # X: [N, F_in]
        H = F.relu(self.gcn1(X, A_hat))
        H = self.dropout(H)
        H = self.gcn2(H, A_hat)
        return F.relu(H)  # [N, out_feats]
    
import torch
import torch.nn as nn
import torch.nn.functional as F

# =============================
#6 Graph Convolution Layer
# =============================
class GCNLayer(nn.Module):
    def __init__(self, in_feats: int, out_feats: int, bias: bool = True):
        super().__init__()
        self.lin = nn.Linear(in_feats, out_feats, bias=bias)

    def forward(self, X: torch.Tensor, A_hat: torch.Tensor) -> torch.Tensor:
        # X: [N, F_in]; A_hat: [N, N]
        return A_hat @ self.lin(X)


# =============================
# Two-layer Spatial GCN
# =============================
class SpatialGCN(nn.Module):
    def __init__(self, in_feats: int, hidden: int, out_feats: int, dropout: float = 0.1):
        super().__init__()
        self.gcn1 = GCNLayer(in_feats, hidden)
        self.gcn2 = GCNLayer(hidden, out_feats)
        self.dropout = nn.Dropout(dropout)

    def forward(self, X: torch.Tensor, A_hat: torch.Tensor) -> torch.Tensor:
        # X: [N, F_in]
        H = F.relu(self.gcn1(X, A_hat))
        H = self.dropout(H)
        H = self.gcn2(H, A_hat)
        return F.relu(H)  # [N, out_feats]


# =============================
# Full STGNN: Spatial + Temporal
# =============================
class STGNN(nn.Module):
    def __init__(self, num_nodes: int, in_feats: int,
                 gcn_hidden: int = 32, gcn_out: int = 32,
                 rnn_hidden: int = 64, horizon: int = 7,
                 dropout: float = 0.1):
        super().__init__()
        self.num_nodes = num_nodes
        self.horizon = horizon
        self.spatial = SpatialGCN(in_feats, gcn_hidden, gcn_out, dropout)
        self.rnn = nn.GRU(input_size=gcn_out, hidden_size=rnn_hidden, batch_first=True)
        self.head = nn.Linear(rnn_hidden, horizon)  # per-node multi-step output
        self.dropout = nn.Dropout(dropout)

    def forward(self, X_seq: torch.Tensor, A_hat: torch.Tensor) -> torch.Tensor:
        """
        X_seq: [B, S, N, F]
        A_hat: [N, N]
        Returns: y_hat [B, H, N]
        """
        B, S, N, F_in = X_seq.shape
        assert N == self.num_nodes

        # Apply spatial GCN at each time step -> [B, S, N, gcn_out]
        gcn_outs = []
        for t in range(S):
            Xt = X_seq[:, t]  # [B, N, F]
            Gt = []
            for b in range(B):
                Hb = self.spatial(Xt[b], A_hat)  # [N, gcn_out]
                Gt.append(Hb.unsqueeze(0))
            Gt = torch.cat(Gt, dim=0)  # [B, N, gcn_out]
            gcn_outs.append(Gt.unsqueeze(1))
        G = torch.cat(gcn_outs, dim=1)  # [B, S, N, gcn_out]

        # Temporal GRU per node
        BN = B * N
        G_reshaped = G.reshape(BN, S, -1)        # [B*N, S, gcn_out]
        _, h_last = self.rnn(G_reshaped)         # h_last: [1, B*N, rnn_hidden]
        HN = h_last.squeeze(0)                   # [B*N, rnn_hidden]
        HN = self.dropout(HN)
        YN = self.head(HN)                       # [B*N, horizon]

        # Reshape back to [B, H, N]
        Y = YN.reshape(B, N, self.horizon).permute(0, 2, 1).contiguous()
        return Y


# =============================
# Example Run
# =============================
if __name__ == "__main__":

    B, S, N, F_in = 2, 14, 5, 3    # batch=2, seq_len=14, num_nodes=5, features=3
    horizon = 7

    X_seq = torch.randn(B, S, N, F_in)
    A_hat = torch.eye(N)  # identity adjacency for testing

    model = STGNN(num_nodes=N, in_feats=F_in, horizon=horizon)
    y_hat = model(X_seq, A_hat)

    print("Input shape:", X_seq.shape)
    print("Adjacency shape:", A_hat.shape)
    print("Output shape:", y_hat.shape)
    print("Sample output:\n", y_hat[0, :, :])    

import os, math
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from dataclasses import dataclass
from typing import Dict, Optional

# Device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# =============================
# TRAIN CONFIG
# =============================
@dataclass
class TrainConfig:
    epochs: int = 50
    batch_size: int = 16
    lr: float = 1e-3
    weight_decay: float = 1e-5
    patience: int = 8
    grad_clip: Optional[float] = 1.0


# =============================
# TRAIN LOOP
# =============================
def ensure_dir(path: str):
    if not os.path.exists(path):
        os.makedirs(path)

def plot_loss_curves(history: Dict, outdir: str):
    import matplotlib.pyplot as plt
    ensure_dir(outdir)
    plt.figure()
    plt.plot(history['train_loss'], label="train")
    plt.plot(history['val_loss'], label="val")
    plt.xlabel("Epoch")
    plt.ylabel("MSE Loss")
    plt.legend()
    plt.title("Training & Validation Loss")
    plt.savefig(os.path.join(outdir, "loss_curve.png"))
    plt.close()

def train_model(model: nn.Module, loaders: Dict[str, DataLoader], A_hat: torch.Tensor,
                cfg: TrainConfig, ckpt_dir: str, plot_dir: str) -> Dict:
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=cfg.lr, weight_decay=cfg.weight_decay)
    best_val = float('inf')
    best_state = None
    history = {"train_loss": [], "val_loss": []}
    patience_left = cfg.patience

    for epoch in range(1, cfg.epochs + 1):
        model.train()
        train_losses = []
        for Xb, yb in loaders['train']:
            Xb, yb = Xb.to(device), yb.to(device)
            optimizer.zero_grad()
            yhat = model(Xb, A_hat)
            loss = criterion(yhat, yb)
            loss.backward()
            if cfg.grad_clip is not None:
                nn.utils.clip_grad_norm_(model.parameters(), cfg.grad_clip)
            optimizer.step()
            train_losses.append(loss.item())

        model.eval()
        val_losses = []
        with torch.no_grad():
            for Xb, yb in loaders['val']:
                Xb, yb = Xb.to(device), yb.to(device)
                yhat = model(Xb, A_hat)
                loss = criterion(yhat, yb)
                val_losses.append(loss.item())

        train_loss = float(np.mean(train_losses)) if train_losses else np.nan
        val_loss = float(np.mean(val_losses)) if val_losses else np.nan
        history['train_loss'].append(train_loss)
        history['val_loss'].append(val_loss)

        print(f"Epoch {epoch:03d} | train MSE {train_loss:.6f} | val MSE {val_loss:.6f}")

        if val_loss < best_val:
            best_val = val_loss
            best_state = {k: v.cpu().clone() for k, v in model.state_dict().items()}
            patience_left = cfg.patience
        else:
            patience_left -= 1
            if patience_left <= 0:
                print("Early stopping triggered.")
                break

    ensure_dir(ckpt_dir)
    best_path = os.path.join(ckpt_dir, "stgnn_best.pt")
    if best_state is not None:
        torch.save(best_state, best_path)
        print(f"Saved best model to {best_path}")
    else:
        print("Warning: No best state captured.")

    plot_loss_curves(history, plot_dir)
    return {"history": history, "best_model_path": best_path}


# =============================
# 7A) EVALUATION (MAE/RMSE/R2) + inverse scaling
# =============================
@torch.no_grad()
def evaluate_model(model: nn.Module, loader: DataLoader, A_hat: torch.Tensor,
                   scaler_y: StandardScaler) -> Dict:
    model.eval()
    y_true_list, y_pred_list = [], []
    for Xb, yb in loader:
        Xb, yb = Xb.to(device), yb.to(device)
        yhat = model(Xb, A_hat)  # [B,H,N]
        y_true_list.append(yb.cpu().numpy())
        y_pred_list.append(yhat.cpu().numpy())

    y_true = np.concatenate(y_true_list, axis=0)
    y_pred = np.concatenate(y_pred_list, axis=0)

    # Inverse scale (target only)
    M, H, N = y_true.shape
    y_true_inv = scaler_y.inverse_transform(y_true.reshape(-1, 1)).reshape(M, H, N)
    y_pred_inv = scaler_y.inverse_transform(y_pred.reshape(-1, 1)).reshape(M, H, N)

    mae = mean_absolute_error(y_true_inv.ravel(), y_pred_inv.ravel())
    rmse = math.sqrt(mean_squared_error(y_true_inv.ravel(), y_pred_inv.ravel()))
    r2 = r2_score(y_true_inv.ravel(), y_pred_inv.ravel())

    return {
        "mae": float(mae),
        "rmse": float(rmse),
        "r2": float(r2),
        "y_true": y_true_inv,
        "y_pred": y_pred_inv,
    }
# Dummy STGNN-like model (just Linear for demo)
class DummySTGNN(nn.Module):
    def __init__(self, N, F, H):
        super().__init__()
        self.fc = nn.Linear(F, H)

    def forward(self, X, A_hat):
        # X: [B,T,N,F] -> take last time step only for demo
        B,T,N,F = X.shape
        out = self.fc(X[:, -1])  # [B,N,H]
        return out.permute(0,2,1)  # [B,H,N]

# Fake data
B,T,N,F,H = 32,5,4,3,1
X_fake = torch.randn(B,T,N,F)
y_fake = torch.randn(B,H,N)

train_loader = DataLoader(list(zip(X_fake, y_fake)), batch_size=8, shuffle=True)
val_loader = DataLoader(list(zip(X_fake, y_fake)), batch_size=8)

loaders = {"train": train_loader, "val": val_loader}

# Adjacency (identity for demo)
A_hat = torch.eye(N).to(device)

# Scaler for inverse transform (fit on true y)
scaler_y = StandardScaler()
scaler_y.fit(y_fake.reshape(-1,1).numpy())

# Train
cfg = TrainConfig(epochs=5)
model = DummySTGNN(N,F,H).to(device)
results = train_model(model, loaders, A_hat, cfg, "checkpoints", "plots")

# Evaluate
eval_results = evaluate_model(model, val_loader, A_hat, scaler_y)
print("Evaluation:", eval_results)
    
#8

import torch
import numpy as np
import math
from torch import nn
from torch.utils.data import DataLoader, TensorDataset
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from typing import Dict

# Device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# =============================
# 1) Dummy ST-GNN model (for demo)
# =============================
class DummySTGNN(nn.Module):
    """Fake model just for testing evaluation loop"""
    def __init__(self, in_dim: int, hidden_dim: int, horizon: int, num_nodes: int):
        super().__init__()
        self.in_dim = in_dim
        self.fc = nn.Linear(in_dim, horizon)   # simple projection

    def forward(self, X: torch.Tensor, A_hat: torch.Tensor):
        # X: [B,L,N,F]
        B, L, N, F = X.shape
        x = X.mean(dim=1)             # aggregate over time -> [B,N,F]
        out = self.fc(x)              # [B,N,H]
        out = out.permute(0,2,1)      # -> [B,H,N]
        return out

# =============================
# 2) Evaluation function
# =============================
@torch.no_grad()
def evaluate_model(model: nn.Module, loader: DataLoader, A_hat: torch.Tensor,
                   scaler_y: StandardScaler) -> Dict:
    model.eval()
    y_true_list, y_pred_list = [], []
    for Xb, yb in loader:
        Xb = Xb.to(device)
        yb = yb.to(device)
        yhat = model(Xb, A_hat)  # [B,H,N]
        y_true_list.append(yb.cpu().numpy())
        y_pred_list.append(yhat.cpu().numpy())

    # stack
    y_true = np.concatenate(y_true_list, axis=0)   # [M,H,N]
    y_pred = np.concatenate(y_pred_list, axis=0)   # [M,H,N]

    # inverse scale
    M, H, N = y_true.shape
    y_true_inv = scaler_y.inverse_transform(y_true.reshape(-1, 1)).reshape(M, H, N)
    y_pred_inv = scaler_y.inverse_transform(y_pred.reshape(-1, 1)).reshape(M, H, N)

    # metrics
    mae = mean_absolute_error(y_true_inv.ravel(), y_pred_inv.ravel())
    rmse = math.sqrt(mean_squared_error(y_true_inv.ravel(), y_pred_inv.ravel()))
    r2 = r2_score(y_true_inv.ravel(), y_pred_inv.ravel())

    return {
        "mae": float(mae),
        "rmse": float(rmse),
        "r2": float(r2),
        "y_true": y_true_inv,
        "y_pred": y_pred_inv,
    }

# =============================
# 3) Example usage
# =============================
if __name__ == "__main__":
    # fake dataset
    num_samples = 100
    L = 12         # input sequence length
    N = 5          # number of regions
    F = 1          # features per node
    H = 3          # forecast horizon

    X = np.random.rand(num_samples, L, N, F)
    y = np.random.rand(num_samples, H, N)

    # scale y
    scaler_y = StandardScaler()
    y_scaled = scaler_y.fit_transform(y.reshape(-1,1)).reshape(num_samples,H,N)

    # convert to tensors
    X_t = torch.tensor(X, dtype=torch.float32)
    y_t = torch.tensor(y_scaled, dtype=torch.float32)

    dataset = TensorDataset(X_t, y_t)
    loader = DataLoader(dataset, batch_size=16, shuffle=False)

    # fake adjacency (identity)
    A_hat = torch.eye(N).to(device)

    # model
    model = DummySTGNN(in_dim=F, hidden_dim=16, horizon=H, num_nodes=N).to(device)

    # evaluate
    results = evaluate_model(model, loader, A_hat, scaler_y)

    print("Evaluation Results:")
    print("MAE :", results["mae"])
    print("RMSE:", results["rmse"])
    print("R²   :", results["r2"])
    
import numpy as np
import pandas as pd
from typing import Tuple

def make_demo_data(N: int = 20, T: int = 260) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Generate synthetic COVID-19 cases and mobility data.

    Parameters:
        N: number of regions
        T: number of days

    Returns:
        df_cases: DataFrame with columns ['date', 'region_id', 'cases']
        df_mob: DataFrame with columns ['date', 'region_id', 'retail','transit','workplace','residential','parks','grocery']
    """
    dates = pd.date_range('2020-03-01', periods=T, freq='D')
    regions = [f'R{i+1}' for i in range(N)]

    rows_c, rows_m = [], []
    base = np.cumsum(np.random.poisson(1.0, size=T))  # base cumulative cases

    for r_idx, r in enumerate(regions):
        noise = np.random.normal(0, 5, size=T)
        trend = base * (0.5 + 0.5 * np.sin((r_idx+1) / N * 2*np.pi))
        cases = np.clip(trend + noise + 10*np.sin(np.arange(T)/14.0 + r_idx), 0, None)
        
        for t, d in enumerate(dates):
            # COVID-19 cases
            rows_c.append((d, r, float(cases[t])))

            # Mobility features
            workplace = 50 + 10*np.sin(t/7.0 + r_idx/3) + np.random.normal(0, 3)
            retail = 40 + 8*np.cos(t/9.0 + r_idx/5) + np.random.normal(0, 3)
            transit = 30 + 12*np.sin(t/10.0 + r_idx/7) + np.random.normal(0, 3)
            parks = 20 + 6*np.cos(t/15.0 + r_idx/4) + np.random.normal(0, 2)
            residential = 60 - 0.3*workplace + np.random.normal(0, 2)
            grocery = 30 + 5*np.sin(t/11.0 + r_idx/6) + np.random.normal(0, 2)
            rows_m.append((d, r, retail, transit, workplace, residential, parks, grocery))

    # Create DataFrames
    df_cases = pd.DataFrame(rows_c, columns=['date','region_id','cases'])
    df_mob = pd.DataFrame(rows_m, columns=['date','region_id','retail','transit','workplace','residential','parks','grocery'])

    return df_cases, df_mob 
df_cases, df_mob = make_demo_data(N=5, T=30)  # 5 regions, 30 days
print("Cases data:")
print(df_cases.head())
print("\nMobility data:")
print(df_mob.head())  

import os
import torch
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
from typing import Dict, List

# ==============================
# 1. Demo Data
# ==============================
def make_demo_data(N=16, T=280):
    import pandas as pd
    import numpy as np
    dates = pd.date_range('2020-03-01', periods=T)
    regions = [f'R{i+1}' for i in range(N)]
    df_c = pd.DataFrame({
        'date': np.repeat(dates, N),
        'region_id': regions * T,
        'cases': np.random.poisson(50, size=T * N)
    })
    df_m = pd.DataFrame({
        'date': np.repeat(dates, N),
        'region_id': regions * T,
        'retail': np.random.rand(T * N),
        'transit': np.random.rand(T * N),
        'workplace': np.random.rand(T * N),
        'residential': np.random.rand(T * N),
        'parks': np.random.rand(T * N),
        'grocery': np.random.rand(T * N)
    })
    return df_c, df_m

def load_and_align(covid_csv, mobility_csv):
    import pandas as pd
    panel = pd.DataFrame()  # dummy
    regions = ["R1", "R2"]
    dates = pd.date_range('2020-03-01', '2020-03-10')
    return panel, regions, dates

# ==============================
# 2. Config Classes
# ==============================
class PreprocessConfig: 
    def __init__(self, feature_cols, target_col, scaler_type, clip_cases_at):
        self.feature_cols = feature_cols
        self.target_col = target_col
        self.scaler_type = scaler_type
        self.clip_cases_at = clip_cases_at

class SplitConfig: 
    def __init__(self, seq_len, horizon, val_ratio, test_ratio):
        self.seq_len = seq_len
        self.horizon = horizon
        self.val_ratio = val_ratio
        self.test_ratio = test_ratio

class GraphConfig: 
    def __init__(self, method, top_k, edges_csv):
        self.method = method
        self.top_k = top_k
        self.edges_csv = edges_csv

class TrainConfig:
    def __init__(self, epochs, batch_size, lr, weight_decay, patience, grad_clip):
        self.epochs = epochs
        self.batch_size = batch_size
        self.lr = lr
        self.weight_decay = weight_decay
        self.patience = patience
        self.grad_clip = grad_clip

# ==============================
# 3. Utils
# ==============================
class Standardizer:
    def __init__(self, mode): 
        self.scaler_y = None
    def fit(self, X, y): pass
    def transform(self, X, y): return X, y

class STWindowDataset(torch.utils.data.Dataset):
    def __init__(self, X, y):
        self.X, self.y = X, y
    def _len_(self): return len(self.X)
    def _getitem_(self, idx): return self.X[idx], self.y[idx]

class STGNN(torch.nn.Module):
    def __init__(self, num_nodes, in_feats, gcn_hidden, gcn_out, rnn_hidden, horizon, dropout):
        super().__init__()
        # dummy simple model: project input features to horizon
        self.fc = torch.nn.Linear(in_feats, horizon)
    def forward(self, X, A_hat):
        # Assume X shape: [B, T, N, F]
        B, T, N, F = X.shape
        out = self.fc(X[:, -1, :, :])  # take last timestep
        return out  # shape [B, N, horizon]

def make_windows(X, y, split_cfg):
    # Dummy split (no real windowing)
    return (X, y), (X, y), (X, y)

def build_adjacency(y_scaled_full, regions, g_cfg):
    N = len(regions)
    A = torch.rand(N, N).numpy()
    return A

def normalize_adjacency(A):
    return A

def train_model(model, loaders, A_hat, tr_cfg, ckpt_dir, plot_dir):
    # dummy training
    path = os.path.join(ckpt_dir, 'best_model.pt')
    torch.save(model.state_dict(), path)
    return {'best_model_path': path}

def evaluate_model(model, loader, A_hat, scaler_y):
    return {
        'mae': 0.5, 
        'rmse': 1.0, 
        'r2': 0.8, 
        'y_true': torch.rand(10, 7, 2).numpy(), 
        'y_pred': torch.rand(10, 7, 2).numpy()
    }

# ==============================
# 4. Plotting
# ==============================
def ensure_dir(path): os.makedirs(path, exist_ok=True)

def plot_region_forecast(eval_out: Dict, regions: List[str], region_idx: int, horizon: int, outdir: str, title_prefix: str=""):
    ensure_dir(outdir)
    y_true = eval_out['y_true']
    y_pred = eval_out['y_pred']
    plt.figure()
    plt.plot(range(1, horizon+1), y_true[:, :, region_idx].mean(axis=0), marker='o', label='Actual')
    plt.plot(range(1, horizon+1), y_pred[:, :, region_idx].mean(axis=0), marker='x', label='Predicted')
    plt.title(f"{title_prefix} {regions[region_idx]}")
    plt.legend()
    plt.show()

def plot_graph(A, regions, outdir, title="Graph"):
    plt.figure()
    plt.imshow(A, cmap='viridis')
    plt.colorbar()
    plt.title(title)
    plt.show()

# ==============================
# 5. Run demo pipeline
# ==============================
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

out_dir = 'runs'
ckpt_dir = os.path.join(out_dir, 'checkpoints'); ensure_dir(ckpt_dir)
plot_dir = os.path.join(out_dir, 'plots'); ensure_dir(plot_dir)

df_c, df_m = make_demo_data(N=4, T=30)
panel, regions, dates = load_and_align(None, None)

X, y, meta = torch.rand(30, 14, 4, 6), torch.rand(30, 4), {}  # dummy features [samples, seq_len, nodes, feats]

split_cfg = SplitConfig(seq_len=14, horizon=7, val_ratio=0.1, test_ratio=0.1)
(Xtr_w, ytr_w), (Xv_w, yv_w), (Xte_w, yte_w) = make_windows(X, y, split_cfg)

ds_train = STWindowDataset(Xtr_w, ytr_w)
ds_val   = STWindowDataset(Xv_w, yv_w)
ds_test  = STWindowDataset(Xte_w, yte_w)
loaders = {
    'train': DataLoader(ds_train, batch_size=4),
    'val': DataLoader(ds_val, batch_size=4),
    'test': DataLoader(ds_test, batch_size=4)
}

A = build_adjacency(y, regions, GraphConfig('corr_topk', 5, None))
A_hat = torch.tensor(normalize_adjacency(A), dtype=torch.float32, device=device)

model = STGNN(num_nodes=4, in_feats=6, gcn_hidden=32, gcn_out=32, rnn_hidden=64, horizon=7, dropout=0.1).to(device)

train_out = train_model(
    model, loaders, A_hat,
    TrainConfig(epochs=2, batch_size=2, lr=1e-3, weight_decay=1e-5, patience=1, grad_clip=1.0),
    ckpt_dir=ckpt_dir, plot_dir=plot_dir
)

eval_out = evaluate_model(model, loaders['test'], A_hat, None)
print("Metrics:", {k: eval_out[k] for k in ['mae','rmse','r2']})

# Plots
plot_region_forecast(eval_out, regions, region_idx=0, horizon=7, outdir=plot_dir)
plot_graph(A, regions, plot_dir)