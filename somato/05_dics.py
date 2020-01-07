import mne
import numpy as np
from config import fname, subject_id

report = mne.open_report(fname.report)

# Create longer epochs
epochs = mne.read_epochs(fname.epochs_long)
freqs = np.logspace(np.log10(5), np.log10(40), 20)

# Compute Cross-Spectral Density matrices
csd = mne.time_frequency.csd_morlet(epochs, frequencies=freqs, tmin=-1, tmax=1.5, decim=5)
csd_baseline = mne.time_frequency.csd_morlet(epochs, frequencies=freqs, tmin=-1, tmax=0, decim=5)
csd_ers = mne.time_frequency.csd_morlet(epochs, frequencies=freqs, tmin=0.5, tmax=1.5, decim=5)

# Compute DICS beamformer to localize ERS
fwd = mne.read_forward_solution(fname.fwd)
inv = mne.beamformer.make_dics(epochs.info, fwd, csd, pick_ori='max-power', noise_csd=csd_baseline)

# Compute source power
stc_baseline, _ = mne.beamformer.apply_dics_csd(csd_baseline, inv)
stc_ers, _ = mne.beamformer.apply_dics_csd(csd_ers, inv)
stc_baseline.subject = subject_id
stc_ers.subject = subject_id

# Normalize with baseline power.
stc_ers /= stc_baseline
stc_ers.data = np.log(stc_ers.data)
stc_ers.save(fname.stc_dics)
fig = stc_ers.plot(subject=subject_id, subjects_dir=fname.subjects_dir, src=fwd['src'],
                   clim=dict(kind='percent', lims=[99, 99.5, 100]))
report.add_figs_to_section(fig, 'DICS Source estimate', 'Source level', replace=True)
report.save(fname.report_html, overwrite=True, open_browser=False)
