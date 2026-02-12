mode = "dev"
monipi_active = "True"
debug_status = True

if mode == "prod":
    reporting_period_in_mins = 5
    secs_between_samples = 60
else:  # dev
    reporting_period_in_mins = 1
    secs_between_samples = 20
