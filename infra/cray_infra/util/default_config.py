from pydantic import BaseModel


class Config(BaseModel):
    api_url: str = "http://localhost:8000"
    #model: str = "diffusion_forcing"
    model: str = "masint/tiny-random-llama"
    #model: str = "meta-llama/Llama-3.2-1B-Instruct"
    #model: str = "HuggingFaceTB/SmolLM-135M"

    # 10GB using 1024 for KB, 1024 for MB, 1024 for GB
    max_upload_file_size: int = 1024 * 1024 * 1024 * 10

    train_job_entrypoint: str = "/app/cray/scripts/train_job_entrypoint.sh"
    training_job_directory: str = "/app/cray/jobs"

    max_train_time: int = 15 * 60
    extra_training_seconds: int = 300  # 5 minutes buffer before slurm kills the job

    slurm_wait_time: int = 30 # seconds

    megatron_refresh_period: int = 30 # seconds

    vllm_api_url: str = "http://localhost:8001"

    generate_batch_size: int = 4

    response_timeout: int = 60 # seconds
    inference_work_queue_timeout: int = 30 # seconds

    inference_work_queue_path: str = "/app/cray/inference_work_queue.sqlite"

    gpu_memory_utilization: float = 0.3
    max_model_length: int = 32768
    dtype: str = "half"

    max_log_length: int = 100

