import numpy as np

from petric import DATA, OUTDIR, SRCDIR, Algorithm, MetricsWithTimeout, QualityMetrics, get_data, get_settings, logging

if __name__ == "__main__":
    from traceback import print_exc

    from tqdm.contrib.logging import logging_redirect_tqdm
    logging.basicConfig(level=logging.INFO)
    redir = logging_redirect_tqdm()
    redir.__enter__()
    from main import Submission, submission_callbacks
    assert issubclass(Submission, Algorithm)
    for src in DATA:
        settings = get_settings(src)
        out = settings.name
        cbk = MetricsWithTimeout(seconds=60 * 60, outdir=OUTDIR / out, **settings.slices, vmax=settings.vmax)
        data = get_data(srcdir=SRCDIR / src, outdir=OUTDIR / out)
        if data.reference_image is not None:
            cbk.callbacks.append(
                QualityMetrics(data.reference_image, data.whole_object_mask, data.background_mask,
                               tb_summary_writer=cbk.tb, voi_mask_dict=data.voi_masks))
        cbk.reset(position=0) # timeout from now
        algo = Submission(data, update_objective_interval=np.iinfo(np.int32).max)
        try:
            algo.run(np.inf, callbacks=[cbk] + submission_callbacks)
        except Exception:
            print_exc(limit=2)
        finally:
            del algo
