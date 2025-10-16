mode = "dev"
monipi_active = "True"

if mode == "prod":
    reporting_period_in_mins = 5
    secs_between_samples = 60
else: # dev
    reporting_period_in_mins = 3
    secs_between_samples = 60

