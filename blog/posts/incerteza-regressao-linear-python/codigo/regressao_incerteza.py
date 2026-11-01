"""Reproduz a regressão e as figuras do artigo (dados de calibração do termopar).

OLS com intercepto: tensões tratadas como conhecidas, erros em temperatura
independentes, de média zero, variância constante e aproximadamente normais.
Intervalos t de 95% são pontuais para a resposta média; não representam uma
avaliação completa da incerteza metrológica da calibração.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import t

TENSAO_MV = np.array([0.20, 1.10, 2.00, 2.90, 4.10, 5.20,
                      6.10, 6.90, 8.20, 8.80, 10.10])
TEMPERATURA_C = np.arange(0.0, 51.0, 5.0)


def incerteza_regressao_linear(x, y, pontos=None, confianca=0.95):
    """Estima OLS e incerteza da resposta média para valores fixos de x."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if x.ndim != 1 or y.ndim != 1 or x.size != y.size or x.size <= 2:
        raise ValueError("Vetores unidimensionais do mesmo tamanho, n > 2")
    if not (np.isfinite(x).all() and np.isfinite(y).all()):
        raise ValueError("Valores devem ser finitos")
    if not 0 < confianca < 1 or np.ptp(x) == 0:
        raise ValueError("Confiança inválida ou tensões idênticas")

    n = len(x)
    A = np.column_stack([np.ones(n), x])
    beta, _, rank, _ = np.linalg.lstsq(A, y, rcond=None)
    if rank != 2:
        raise ValueError("Matriz de planejamento sem posto completo")

    y_ajustado = A @ beta
    residuos = y - y_ajustado
    sqr = float(residuos @ residuos)
    gl = n - 2
    s2 = sqr / gl
    _, R = np.linalg.qr(A, mode="reduced")
    Rinv = np.linalg.solve(R, np.eye(2))
    C = s2 * (Rinv @ Rinv.T)

    xp = x if pontos is None else np.asarray(pontos, dtype=float).reshape(-1)
    if not np.isfinite(xp).all():
        raise ValueError("Pontos de avaliação devem ser finitos")
    B = np.column_stack([np.ones(xp.size), xp])
    ym = B @ beta
    u2 = np.einsum("ij,jk,ik->i", B, C, B)
    u_media = np.sqrt(np.maximum(0, u2))
    k = float(t.ppf((1 + confianca) / 2, gl))
    r2 = 1 - sqr / np.sum((y - y.mean()) ** 2)

    return {
        "coeficientes": beta,
        "covariancia": C,
        "x": xp,
        "y_media": ym,
        "residuos": residuos,
        "r2": r2,
        "desvio_padrao_residual": np.sqrt(s2),
        "rmse": np.sqrt(sqr / n),
        "graus_liberdade": gl,
        "fator_abrangencia": k,
        "u_media": u_media,
        "U_media": k * u_media,
        "u_pred": np.sqrt(u_media**2 + s2),
        "U_pred": k * np.sqrt(u_media**2 + s2),
    }


def salvar_figura(pasta, nome):
    plt.tight_layout()
    plt.savefig(pasta / f"{nome}.svg", bbox_inches="tight")
    plt.savefig(pasta / f"{nome}.png", dpi=190, bbox_inches="tight")
    plt.close()


def main():
    x, y = TENSAO_MV, TEMPERATURA_C
    r = incerteza_regressao_linear(x, y)
    xp = np.linspace(x.min(), x.max(), 401)
    curva = incerteza_regressao_linear(x, y, pontos=xp)
    pasta = Path(__file__).resolve().parent.parent / "figuras"
    pasta.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(8, 4.6))
    plt.scatter(x, y, label="Dados da calibração", zorder=3)
    plt.plot(xp, curva["y_media"], label="Regressão linear")
    plt.fill_between(xp, curva["y_media"] - curva["U_media"],
                     curva["y_media"] + curva["U_media"], alpha=.18,
                     label="IC 95% da média (pontual)")
    plt.xlabel("Tensão (mV)")
    plt.ylabel("Temperatura (°C)")
    plt.title("Regressão linear: calibração de termopar")
    plt.grid(alpha=.2)
    plt.legend(loc="upper left", frameon=True)
    salvar_figura(pasta, "01_regressao_e_incerteza")

    plt.figure(figsize=(8, 4.2))
    plt.scatter(x, r["residuos"], zorder=3)
    plt.axhline(0, ls="--", lw=1.2)
    plt.xlabel("Tensão (mV)")
    plt.ylabel("Resíduo (°C)")
    plt.title("Resíduos da regressão")
    plt.grid(alpha=.2)
    salvar_figura(pasta, "02_residuos")

    plt.figure(figsize=(8, 4.2))
    plt.plot(xp, curva["u_media"], label="Incerteza-padrão da média")
    plt.plot(xp, curva["U_media"], label="Incerteza expandida 95%")
    plt.xlabel("Tensão (mV)")
    plt.ylabel("Incerteza (°C)")
    plt.title("Incerteza da resposta média")
    plt.grid(alpha=.2)
    plt.legend(loc="upper center", frameon=True)
    salvar_figura(pasta, "03_incerteza_por_tensao")

    b0, b1 = r["coeficientes"]
    print(f"T = {b1:.8f} V + ({b0:.8f}) °C")
    print(f"R² = {r['r2']:.8f}")
    print(f"Desvio-padrão residual = {r['desvio_padrao_residual']:.8f} °C")
    print(f"RMSE = {r['rmse']:.8f} °C")
    print(f"gl = {r['graus_liberdade']}, k = {r['fator_abrangencia']:.8f}")
    print(f"u_m nos pontos: {r['u_media'].min():.6f} a {r['u_media'].max():.6f} °C")
    print(f"U_m nos pontos: {r['U_media'].min():.6f} a {r['U_media'].max():.6f} °C")


if __name__ == "__main__":
    main()
