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

#!/usr/bin/env python3

import aws_cdk as core
from constructs import Construct

from CodeCommit import CodeCommitStack
from CodeBuildECR import CodeBuildECRStack
from CodePipeline import CodePipelineStack
from BatchEnv import BatchEnvironment


class CICDSoftwarePipeline(Construct):
    def __init__(self, scope, id, assets_directory):
        super().__init__(scope, id)

        # build the repository
        code = CodeCommitStack(app, f"{id}-code", id, assets_directory)

        # create the build project and associated artifacts directories
        build = CodeBuildECRStack(app, f"{id}-build", id)
        build.add_dependency(code)

        # build the pipeline stage
        pipeline = CodePipelineStack(app, f"{id}-pipeline", id)
        pipeline.add_dependency(build)

        batch = BatchEnvironment(app, f"{id}-batch", id)
        batch.add_dependency(build)


app = core.App()
CICDSoftwarePipeline(app, "CICDPipelineAWSBatch", 'app-package')
app.synth()
