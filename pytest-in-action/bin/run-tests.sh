#!/bin/sh
pytest src/tests \
            --junitxml=reports/test_results.xml \
            --html=reports/test_results.html \
            --self-contained-html -v