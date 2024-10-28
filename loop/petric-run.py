#!/usr/bin/env python
import os

os.environ['PETRIC_SKIP_DATA'] = '1'

from petric import DATA_SLICES, OUTDIR, SRCDIR, Algorithm, MetricsWithTimeout, QualityMetrics, get_data, logging, np

data_dirs_metrics = [
    (SRCDIR / "Siemens_Vision600_Hoffman", OUTDIR / "Vision600_Hoffman",
     [MetricsWithTimeout(outdir=OUTDIR / "Vision600_Hoffman", **DATA_SLICES['Siemens_Vision600_Hoffman'])]),
    (SRCDIR / "NeuroLF_Esser_Dataset", OUTDIR / "NeuroLF_Esser",
     [MetricsWithTimeout(outdir=OUTDIR / "NeuroLF_Esser", **DATA_SLICES['NeuroLF_Esser_Dataset'])]),
    (SRCDIR / "Siemens_Vision600_ZrNEMAIQ", OUTDIR / "Vision600_ZrNEMA",
     [MetricsWithTimeout(outdir=OUTDIR / "Vision600_ZrNEMA", **DATA_SLICES['Siemens_Vision600_ZrNEMAIQ'])]),
    (SRCDIR / "GE_D690_NEMA_IQ", OUTDIR / "D690_NEMA",
     [MetricsWithTimeout(outdir=OUTDIR / "D690_NEMA", **DATA_SLICES['GE_D690_NEMA_IQ'])]),
    (SRCDIR / "Mediso_NEMA_IQ_lowcounts", OUTDIR / "Mediso_NEMA_lowcounts",
     [MetricsWithTimeout(outdir=OUTDIR / "Mediso_NEMA_lowcounts", **DATA_SLICES['Mediso_NEMA_IQ_lowcounts'])]),
    (SRCDIR / "GE_DMI4_NEMA_IQ", OUTDIR / "DMI4_NEMA",
     [MetricsWithTimeout(outdir=OUTDIR / "DMI4_NEMA", **DATA_SLICES['GE_DMI4_NEMA_IQ'])])]

if __name__ == "__main__":
    from traceback import print_exc

    from tqdm.contrib.logging import logging_redirect_tqdm
    logging.basicConfig(level=logging.INFO)
    redir = logging_redirect_tqdm()
    redir.__enter__()
    from main import Submission, submission_callbacks
    assert issubclass(Submission, Algorithm)
    for srcdir, outdir, metrics in data_dirs_metrics:
        data = get_data(srcdir=srcdir, outdir=outdir)
        metrics_with_timeout = metrics[0]
        if data.reference_image is not None:
            metrics_with_timeout.callbacks.append(
                QualityMetrics(data.reference_image, data.whole_object_mask, data.background_mask,
                               tb_summary_writer=metrics_with_timeout.tb, voi_mask_dict=data.voi_masks))
        metrics_with_timeout.reset() # timeout from now
        algo = Submission(data)
        try:
            algo.run(np.inf, callbacks=metrics + submission_callbacks, update_objective_interval=np.inf)
        except Exception:
            print_exc(limit=2)
        finally:
            del algo
