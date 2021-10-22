import logging
import os
import random
import sys

from simulation import Simulation


assert (
    os.path.basename(os.getcwd()).split("/")[-1] == "model"
), "The script currently uses relative paths, unfortunately"


REPORT_FILENAME = os.getenv("REPORT_FILENAME", None)
PLOT_FILENAME = os.getenv("PLOT_FILENAME", None)
PROFILE_FILENAME = os.getenv("PROFILE_FILENAME", None)
N_STK = os.getenv("N_STK", 7)
N_MAN = os.getenv("N_MAN", 3)
LOCKTIME = os.getenv("LOCKTIME", 24)
HIST_CSV = os.getenv("HIST_CSV", "../block_fees/historical_fees.csv")
RESERVE_STRAT = os.getenv("RESERVE_STRAT", "CUMMAX95Q90")
FALLBACK_EST_STRAT = os.getenv("FALLBACK_EST_STRAT", "85Q1H")
CF_COIN_SELECTION = os.getenv("CF_COIN_SELECTION", 3)
CANCEL_COIN_SELECTION = os.getenv("CANCEL_COIN_SELECTION", 1)
NUMBER_VAULTS = os.getenv("NUMBER_VAULTS", 10)
REFILL_EXCESS = os.getenv("REFILL_EXCESS", 2)
REFILL_PERIOD = os.getenv("REFILL_PERIOD", 1008)
# Unvault rate per day
UNVAULT_RATE = os.getenv("UNVAULT_RATE", 0.5)
# Invalid rate per unvault
INVALID_SPEND_RATE = os.getenv("INVALID_SPEND_RATE", 0.01)
# Catastrophe rate per day
CATASTROPHE_RATE = os.getenv("CATASTROPHE_RATE", 0.001)
# Delegate rate per day (if not running at fixed scale)
DELEGATE_RATE = os.getenv("DELEGATE_RATE", None)

# Plot types
PLOT_BALANCE = bool(int(os.getenv("PLOT_BALANCE", 1)))
PLOT_CUM_OP_COST = bool(int(os.getenv("PLOT_CUM_OP_COST", 1)))
PLOT_RISK_TIME = bool(int(os.getenv("PLOT_RISK_TIME", 0))) and PLOT_CUM_OP_COST
PLOT_DIVERGENCE = bool(int(os.getenv("PLOT_DIVERGENCE", 0)))
PLOT_OP_COST = bool(int(os.getenv("PLOT_OP_COST", 0)))
PLOT_OVERPAYMENTS = bool(int(os.getenv("PLOT_OVERPAYMENTS", 0)))
PLOT_RISK_STATUS = bool(int(os.getenv("PLOT_RISK_STATUS", 0)))
PLOT_FB_COINS_DIST = bool(int(os.getenv("PLOT_FB_COINS_DIST", 0)))

LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG").upper()

if __name__ == "__main__":
    random.seed(21000000)

    if LOG_LEVEL in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        logging.basicConfig(level=LOG_LEVEL)
    else:
        logging.basicConfig(level=logging.DEBUG)
        logging.error("Invalid log level provided, setting as DEBUG instead.")

    req_vars = [
        N_STK,
        N_MAN,
        LOCKTIME,
        HIST_CSV,
        RESERVE_STRAT,
        FALLBACK_EST_STRAT,
        CF_COIN_SELECTION,
        CANCEL_COIN_SELECTION,
        NUMBER_VAULTS,
        REFILL_EXCESS,
        REFILL_PERIOD,
        UNVAULT_RATE,
        INVALID_SPEND_RATE,
        CATASTROPHE_RATE,
    ]
    if any(v is None for v in req_vars):
        logging.error(
            "Need all these environment variables to be set: N_STK, N_MAN, LOCKTIME,"
            " HIST_CSV, RESERVE_STRAT, FALLBACK_EST_STRAT, CF_COIN_SELECTION,"
            " CANCEL_COIN_SELECTION, NUMBER_VAULTS, REFILL_EXCESS,"
            " REFILL_PERIOD, UNVAULT_RATE, INVALID_SPEND_RATE, CATASTROPHE_RATE."
        )
        sys.exit(1)

    plot_types = [
        PLOT_BALANCE,
        PLOT_CUM_OP_COST,
        PLOT_DIVERGENCE,
        PLOT_OP_COST,
        PLOT_OVERPAYMENTS,
        PLOT_RISK_STATUS,
        PLOT_FB_COINS_DIST,
    ]
    if len([plot for plot in plot_types if plot is True]) < 2:
        logging.error(
            "Must generate at least two plot types to run simulation. Plot types are:"
            " PLOT_BALANCE, PLOT_CUM_PLOT_OP_COST, PLOT_DIVERGENCE, PLOT_OP_COST,"
            " PLOT_OVERPAYMENTS, PLOT_RISK_STATUS, or PLOT_FB_COINS_DIST."
        )
        sys.exit(1)

    configuration = {
        "REPORT_FILENAME": REPORT_FILENAME,
        "PLOT_FILENAME": PLOT_FILENAME,
        "PROFILE_FILENAME": PROFILE_FILENAME,
        "N_STK": N_STK,
        "N_MAN": N_MAN,
        "LOCKTIME": LOCKTIME,
        "HIST_CSV": HIST_CSV,
        "RESERVE_STRAT": RESERVE_STRAT,
        "FALLBACK_EST_STRAT": FALLBACK_EST_STRAT,
        "CF_COIN_SELECTION": CF_COIN_SELECTION,
        "CANCEL_COIN_SELECTION": CANCEL_COIN_SELECTION,
        "NUMBER_VAULTS": NUMBER_VAULTS,
        "REFILL_EXCESS": REFILL_EXCESS,
        "REFILL_PERIOD": REFILL_PERIOD,
        "UNVAULT_RATE": UNVAULT_RATE,
        "INVALID_SPEND_RATE": INVALID_SPEND_RATE,
        "CATASTROPHE_RATE": CATASTROPHE_RATE,
        "DELEGATE_RATE": DELEGATE_RATE,
    }
    logging.info(f"Configuration:\n{configuration}")

    sim = Simulation(
        int(N_STK),
        int(N_MAN),
        int(LOCKTIME),
        HIST_CSV,
        RESERVE_STRAT,
        FALLBACK_EST_STRAT,
        int(CF_COIN_SELECTION),
        int(CANCEL_COIN_SELECTION),
        int(NUMBER_VAULTS),
        int(REFILL_EXCESS),
        int(REFILL_PERIOD),
        float(UNVAULT_RATE),
        float(INVALID_SPEND_RATE),
        float(CATASTROPHE_RATE),
        float(DELEGATE_RATE) if DELEGATE_RATE is not None else None,
        with_balance=PLOT_BALANCE,
        with_divergence=PLOT_DIVERGENCE,
        with_op_cost=PLOT_OP_COST,
        with_cum_op_cost=PLOT_CUM_OP_COST,
        with_risk_time=PLOT_RISK_TIME,
        with_overpayments=PLOT_OVERPAYMENTS,
        with_risk_status=PLOT_RISK_STATUS,
        with_fb_coins_dist=PLOT_FB_COINS_DIST,
    )

    start_block = 350000
    end_block = 681000

    if PROFILE_FILENAME is not None:
        import pstats
        from pstats import SortKey
        import cProfile

        cProfile.run("sim.run(start_block, end_block)", f"{PROFILE_FILENAME}")
        p = pstats.Stats(f"{PROFILE_FILENAME}")
        stats = p.strip_dirs().sort_stats(SortKey.CUMULATIVE).print_stats()

    else:
        sim.run(start_block, end_block)

        report = sim.plot(PLOT_FILENAME, True)[0]
        logging.info(f"Report\n{report}")

        if REPORT_FILENAME is not None:
            with open(f"{REPORT_FILENAME}.txt", "w+", encoding="utf-8") as f:
                f.write(report)
