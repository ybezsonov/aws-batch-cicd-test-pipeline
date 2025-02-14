# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from aws_cdk import (
    aws_s3,
    aws_codepipeline,
    aws_ecr,
    aws_ssm,
    aws_codecommit,
    aws_codebuild,
    aws_codepipeline_actions
)
import aws_cdk as core
from constructs import Construct

class CodePipelineStack(core.Stack):

    def __init__(self, scope: Construct, id: str, namespace, ** kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # get repository name
        repository_name = aws_ssm.StringParameter.value_for_string_parameter(
            self, f"{namespace}-repository")

        # get repository reference
        code_repository = aws_codecommit.Repository.from_repository_name(
            scope=self, id=f"codecommit-repository-{id}", repository_name=repository_name)

        # get codebuild project name
        buildproject_name = aws_ssm.StringParameter.value_for_string_parameter(
            self, f"{namespace}-codebuild")

        # get build project reference
        build_project = aws_codebuild.PipelineProject.from_project_name(
            scope=self, id=f"codebuild-project-{id}", project_name=buildproject_name)

        # get codebuild project name
        source_bucket_name = aws_ssm.StringParameter.value_for_string_parameter(
            self, f"{namespace}-sourcebucket")

        # get build project reference
        source_bucket = aws_s3.Bucket.from_bucket_name(
            scope=self, id=f"artifacts-bucket-{id}", bucket_name=source_bucket_name)

        # define the s3 artifact
        artifacts_bucket = aws_codepipeline.Artifact(artifact_name='source')
        # define the pipeline
        pipeline = aws_codepipeline.Pipeline(
            self, "CodePipeline",
            pipeline_name=f"{namespace}",
            artifact_bucket=source_bucket,
            stages=[
                aws_codepipeline.StageProps(
                    stage_name='Source',
                    actions=[
                        aws_codepipeline_actions.CodeCommitSourceAction(
                            repository=code_repository,
                            branch='main',
                            action_name='CodeCommitSourceRetrieval',
                            output=artifacts_bucket,
                        ),
                    ]
                ),
                aws_codepipeline.StageProps(
                    stage_name='Build',
                    actions=[
                        aws_codepipeline_actions.CodeBuildAction(
                            action_name='DockerBuildImages',
                            input=artifacts_bucket,
                            project=build_project,
                        )
                    ]
                )
            ]

        )

        source_bucket.grant_read_write(pipeline.role)

        # pipeline param to get the
        pipeline_param = aws_ssm.StringParameter(
            self, "CodePipelineName",
            parameter_name=f"{namespace}-pipeline",
            string_value=pipeline.pipeline_name,
            description='Code Pipeline Name'
        )
        # cfn output
        core.CfnOutput(
            self, "PipelineName",
            description="CodePipeline Name",
            value=pipeline.pipeline_name
        )

    # # pass objects to another stack
    # @property
    # def outputs(self):
    #     return self.output_props
