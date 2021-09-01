#!/usr/bin/env python3

from aws_cdk import core

from cdk_lambda_powertools_idempotency.cdk_lambda_powertools_idempotency_stack import CdkLambdaPowertoolsIdempotencyStack


app = core.App()
CdkLambdaPowertoolsIdempotencyStack(app, "cdk-lambda-powertools-idempotency")

app.synth()
