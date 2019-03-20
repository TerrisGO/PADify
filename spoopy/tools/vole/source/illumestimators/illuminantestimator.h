/*	
	Copyright(c) 2012 Christian Riess <christian.riess@cs.fau.de>
	and Johannes Jordan <johannes.jordan@cs.fau.de>.

	This file may be licensed under the terms of of the GNU General Public
	License, version 3, as published by the Free Software Foundation. You can
	find it here: http://www.gnu.org/licenses/gpl.html
*/

#ifndef ILLUMESTIMATORS_ILLUMINANTESTIMATOR_H
#define ILLUMESTIMATORS_ILLUMINANTESTIMATOR_H

#include "illum.h"
#include "superpixel.h"
#include <opencv2/core/core.hpp>
#include <vector>

namespace illumestimators {

/** The IlluminantEstimator class provides a base class for illuminant estimation algorithms. */
class IlluminantEstimator
{
public:
	IlluminantEstimator();
	virtual ~IlluminantEstimator();

public:
	/** Estimate the dominant illuminant of an image.
	 *  \param image Input image in BGR format.
	 *  \return Illuminant chromaticities vector in BGR format.
	 */
	virtual Illum estimateIlluminant(const cv::Mat_<cv::Vec3d>& image) const;
	/** Estimate the dominant illuminant of an image.
	 *  \param image Input image in BGR format.
	 *  \param mask Image mask.
	 *  \return Illuminant chromaticities vector in BGR format.
	 */
	virtual Illum estimateIlluminant(const cv::Mat_<cv::Vec3d>& image, const cv::Mat_<unsigned char>& mask) const = 0;
	/** Estimate the dominant illuminant of a superpixel of an image.
	 *  \param image Input image in BGR format.
	 *  \param superpixel Image coordinates of the superpixel.
	 *  \param mask Image mask.
	 *  \return Illuminant chromaticities vector in BGR format.
	 */
	virtual Illum estimateIlluminant(const cv::Mat_<cv::Vec3d>& image, const superpixels::Superpixel& superpixel) const;
	/** Estimate the dominant illuminant of a superpixel of an image.
	 *  \param image Input image in BGR format.
	 *  \param superpixel Superpixel used for estimation.
	 *  \param mask Image mask.
	 *  \return Illuminant chromaticities vector in BGR format.
	 */
	virtual Illum estimateIlluminant(const cv::Mat_<cv::Vec3d>& image, const superpixels::Superpixel& superpixel, const cv::Mat_<unsigned char>& mask) const;
	/** Estimate the dominant illuminant of a set of superpixel of an image.
	 *  \param image Input image in BGR format.
	 *  \param superpixels Vector of superpixels used for estimation.
	 *  \param estimatedIlluminants Vector of illuminant estimates per superpixel.
	 *  \param mask Image mask.
	 */
	virtual void estimateIlluminants(const cv::Mat_<cv::Vec3d>& image, const std::vector<superpixels::Superpixel>& superpixels, std::vector<Illum>& estimatedIlluminants, const cv::Mat_<unsigned char>& mask) const;

public:
	/** Run pre-processing on the image and mask.
	 *  \param image Input image in BGR format.
	 *  \param mask Input mask.
	 *  \param outputImage Pre-processed image.
	 *  \param outputMask Pre-processed mask.
	 */
	virtual void preprocessImage(const cv::Mat_<cv::Vec3d>& image, const cv::Mat_<unsigned char>& mask, cv::Mat_<cv::Vec3d>& outputImage, cv::Mat_<unsigned char>& outputMask) const = 0;

public:
	/** Name of illuminant estimator with current parameters for display purposes.
	 *  \return Name of illuminant estimator.
	 */
	virtual std::string name() const = 0;
	/** Unique identifier of illuminant estimator given current parameters.
	 *  \return Unique identifier of illuminant estimator.
	 */
	virtual std::string identifier() const = 0;

public:
	static cv::Mat_<cv::Vec3d> cleanlyReadImage(const std::string &imageFile, const std::string &colorspace, int verbosity = 0);
	virtual int error() = 0;
};

} // namespace illumestimators

#endif // ILLUMESTIMATORS_ILLUMINANTESTIMATOR_H
