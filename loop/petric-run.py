from petric import DATA_SLICES, OUTDIR, SRCDIR, Algorithm, MetricsWithTimeout, QualityMetrics, get_data, logging, np

shortnames = {
    "Siemens_Vision600_thorax": "Vision600_thorax",
    "Siemens_Vision600_Hoffman": "Vision600_Hoffman",
    "NeuroLF_Esser_Dataset": "NeuroLF_Esser",
    "Siemens_Vision600_ZrNEMAIQ": "Vision600_ZrNEMA",
    "GE_D690_NEMA_IQ": "D690_NEMA",
    "Mediso_NEMA_IQ": "Mediso_NEMA",
    "GE_DMI3_Torso": "DMI3_Torso",
    "GE_DMI4_NEMA_IQ": "DMI4_NEMA",
}

if __name__ == "__main__":
    from traceback import print_exc

    from tqdm.contrib.logging import logging_redirect_tqdm
    logging.basicConfig(level=logging.INFO)
    redir = logging_redirect_tqdm()
    redir.__enter__()
    from main import Submission, submission_callbacks
    assert issubclass(Submission, Algorithm)
    for src, out in shortnames.items():
        data = get_data(srcdir=SRCDIR / src, outdir=OUTDIR / out)
        cbk = MetricsWithTimeout(outdir=OUTDIR / out, **DATA_SLICES[src])
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
