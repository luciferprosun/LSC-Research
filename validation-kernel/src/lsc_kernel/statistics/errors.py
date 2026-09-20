"""Errors specific to the independent statistical engine."""


class StatisticalEngineError(RuntimeError):
    pass


class StatisticalInputError(StatisticalEngineError):
    pass


class CovarianceValidationError(StatisticalEngineError):
    pass


class SingularCovarianceError(CovarianceValidationError):
    pass


class CovarianceScenarioUnavailable(CovarianceValidationError):
    pass


class MetricPrerequisiteError(StatisticalEngineError):
    pass


class BaselineSpecificationIncomplete(StatisticalEngineError):
    pass


class DataLeakageError(StatisticalEngineError):
    pass


class LSCStatisticalExecutionForbidden(StatisticalEngineError):
    pass
