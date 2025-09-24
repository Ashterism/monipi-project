mode = "dev"

if mode == "prod":
    samples_to_average = 5
    secs_between_samples = 60
else: # dev
    samples_to_average = 10
    secs_between_samples = 1.5

