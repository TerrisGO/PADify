vole_module_name("illumestimators")
vole_module_description("Illuminant Estimation Algorithms")
vole_module_variable("Vole_IllumEstimators")

vole_add_required_dependencies("OPENCV" "BOOST" "BOOST_PROGRAM_OPTIONS" "BOOST_SERIALIZATION")
vole_add_required_modules(rbase superpixels rbase computational_geometry)

vole_compile_library(
	commands/grayworldcommand.cpp
	commands/grayworldcommand.h
	commands/grayworldconfig.cpp
	commands/grayworldconfig.h
	commands/bayesiancommand.cpp
	commands/bayesiancommand.h
	commands/bayesianconfig.cpp
	commands/bayesianconfig.h
)

vole_add_command("grayworld" "commands/grayworldcommand.h"             "illumestimators::GrayWorldCommand")
vole_add_command("bayesian" "commands/bayesiancommand.h"             "illumestimators::BayesianCommand")

vole_compile_library(
	illuminantestimator.cpp
	illuminantestimator.h

	baseline/meanestimator.cpp
	baseline/meanestimator.h
	baseline/nothingestimator.cpp
	baseline/nothingestimator.h

	grayworld/grayworldestimator.cpp
	grayworld/grayworldestimator.h

	bayesian/bayesianestimator.cpp
	bayesian/bayesianestimator.h

	common/color.cpp
	common/color.h
	common/convexhull.h
	common/convexpolygon.cpp
	common/convexpolygon.h
	common/derivative.cpp
	common/derivative.h
	common/illuminant_estimator_loader.cpp
	common/illuminant_estimator_loader.h
	common/linesegment.cpp
	common/linesegment.h
	common/mask.cpp
	common/mask.h
	common/scale.h
	common/statistics.cpp
	common/statistics.h

	evaluation/error.cpp
	evaluation/error.h
	evaluation/error2.cpp
	evaluation/error2.h
	evaluation/crossvalidation.cpp
	evaluation/crossvalidation.h
	evaluation/evaluationreport.cpp
	evaluation/evaluationreport.h

	fusion/fusion.h
	fusion/fusion.cpp
	fusion/histogramVoting/histogramVotingFusion.cpp
	fusion/histogramVoting/histogramVotingFusion.h
	fusion/histogramVoting/config_histogram_voting_fusion.cpp
	fusion/histogramVoting/config_histogram_voting_fusion.h

	metadata/metadata.cpp
	metadata/metadata.h
	metadata/metadatastorage.cpp
	metadata/metadatastorage.h

	pipeline/single_illuminant_pipeline.cpp
	pipeline/single_illuminant_pipeline.h
)

vole_add_module()
