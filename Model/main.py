import logging
import os
import random

from simulation import Simulation

REPORT_FILENAME = os.getenv("REPORT_FILENAME", None)
PLOT_FILENAME = os.getenv("PLOT_FILENAME", None)

if __name__ == "__main__":
    random.seed(21000000)
    # FIXME: make it configurable through command line
    logging.basicConfig(level=logging.DEBUG)

    # FIXME: make it configurable through command line
    # note: fee_estimates_fine.csv starts on block 415909 at 2016-05-18 02:00:00
    config = {
        "n_stk": 7,
        "n_man": 3,
        "reserve_strat": "CUMMAX95Q90",
        "estimate_strat": "ME30",
        "O_version": 1,
        "I_version": 2,
        "feerate_src": "../block_fees/historical_fees.csv",
        "estimate_smart_feerate_src": "fee_estimates_fine.csv",
        "weights_src": "tx_weights.csv",
        "block_datetime_src": "block_height_datetime.csv",
    }
    logging.info(f"Using config {config}")

    sim = Simulation(
        config,
        with_balance=True,
        with_vault_excess=True,
        with_cum_op_cost=True,
        with_overpayments=True,
    )

    start_block = 200000
    end_block = 681000

    sim.run(start_block, end_block)
    report = sim.plot(PLOT_FILENAME)
    logging.info(f"Report\n{report}")

    if REPORT_FILENAME is not None:
        with open(REPORT_FILENAME, "w+", encoding="utf-8") as f:
            f.write(report)