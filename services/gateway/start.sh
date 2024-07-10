#!/bin/bash

set -e
set -x
set -o pipefail

uvicorn main:app --host 0.0.0.0 --port 8000 --reload
