import boto3
import time

def lambda_handler(event, context):
    conn = boto3.client("emr")
    # chooses the first cluster which is Running or Waiting
    # possibly can also choose by name or already have the cluster id
    clusters = conn.list_clusters()
    # choose the correct cluster
    clusters = [c["Id"] for c in clusters["Clusters"] 
                if c["Status"]["State"] in ["RUNNING", "WAITING"]]
    if not clusters:
        sys.stderr.write("No valid clusters\n")
        sys.stderr.exit()
    # take the first relevant cluster
    cluster_id = clusters[0]
    
    
    # code location on your emr master node
    # CODE_DIR = "/home/hadoop/code/"



    # spark-submit s3://cc-final-proj/ALSForUid.py s3://cc-final-proj/data_part2.txt 1488844
    
    # spark configuration example
    # step_args = ["/usr/bin/spark-submit", "--spark-conf", "your-configuration",
    #              CODE_DIR + "your_file.py", '--your-parameters', 'parameters']
    
    step_args = ["/usr/bin/spark-submit", "s3://cc-final-proj/ALSForUid-2.py", "s3://cc-final-proj/data_part2_test_new.txt", '6000']

    step = {"Name": "test_job" + time.strftime("%Y%m%d-%H:%M"),
            'ActionOnFailure': 'CONTINUE',
            'HadoopJarStep': {
                'Jar': 's3n://elasticmapreduce/libs/script-runner/script-runner.jar',
                'Args': step_args
            }
        }
    action = conn.add_job_flow_steps(JobFlowId=cluster_id, Steps=[step])
    return "Added step: %s"%(action)
