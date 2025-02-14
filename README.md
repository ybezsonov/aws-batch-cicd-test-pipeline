# CI/CD Test Pipeline on AWS Batch

This project deploys an architecture providing a CI/CD pipeline that will package an application into a container when code is pushed to a Git repository. It will then trigger a job on AWS Batch using the newly produced container.

This pipeline can be used to develop and test your application in the same environment you would be using in production.

## Architecture

This architecture has been built with the [AWS CDK](https://aws.amazon.com/cdk/)
and make use of the following services:

- [AWS CodeCommit](https://aws.amazon.com/codecommit/) as the repository manager.
- [AWS CodeBuild](https://aws.amazon.com/codebuild/) to build the container.
- [AWS CodePipeline](https://aws.amazon.com/codepipeline/) to orchestrate the build pipeline.
- [Amazon ECR](https://aws.amazon.com/ecr/) as the container registry manager.
- [AWS EventBridge](https://aws.amazon.com/eventbridge/) to trigger job submission when containers are stored.
- [AWS Batch](https://aws.amazon.com/batch/) to run the jobs.
- [Amazon Virtual Private Cloud](https://aws.amazon.com/vpc/) to deploy instances that will be running the jobs.

The AWS CDK stack deploys a source code repository, the pipeline with the build workflow, an Amazon ECR repository, a rule to trigger a job when a new container is stored on the repository, an AWS Batch Compute Environment as well as a Job Queue and a Job Definition and, a VPC in which instances will be residing.

![architecture](./doc/ci-cd-diagram.png)

## How to Deploy

To deploy this architecture, you will need to follow these steps:

1. Create a virtual env and activate it
```
git clone https://github.com/aws-samples/aws-batch-cicd-test-pipeline.git
cd aws-batch-cicd-test-pipeline
python3 -m venv .env
source .env/bin/activate
```
2. Install the required dependencies
```
pip install -r requirements.txt
```
3. Provisioning resources for the AWS CDK before you can deploy AWS CDK apps into an AWS environment
```
cdk bootstrap
```
4. Synthesize the CloudFormation template
```
cdk synth
```
5. Deploy the stack
```
cdk deploy '*' --require-approval never
```

Your stack will take a few minutes to deploy. The code in the directory `app-package` will be uploaded and added to your *AWS CodeCommit* repository.

## Clean Up

```
cdk destroy '*' -f
```

## Extending the Stack

You can extend the stack to modify the following components:

- Code repository: use Github or Bitbucket.
- Build Pipeline: add other stages, for example to include static code analysis or run tests as part of the integration workflow.
- Job submission: run [Array Jobs](https://docs.aws.amazon.com/batch/latest/userguide/array_jobs.html) instead of a single job.
- Job Execution: replace AWS Batch by another service such as Amazon ECS, Amazon EKS or AWS ParallelCluster.

You could also integrate an [Amazon Lambda](https://aws.amazon.com/lambda/) function as a target of the Job Submission Rule if you want to integrate additional logic on the job submission process.

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.
