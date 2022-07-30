from hydra.experimental import initialize, compose

from waka_variable import Results

with initialize(config_path="../param"):
    hyparam = compose(config_name="test.yml")

Results(config=hyparam)
