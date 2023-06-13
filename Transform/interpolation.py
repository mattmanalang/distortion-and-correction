class interpolation:

    def linear_interpolation(self, x, Pt1, I_Pt1, Pt2, I_Pt2):
        """Computes the linear interpolation value at some iD location x between two 1D points (Pt1 and Pt2).
        
        There are no arguments defined in the function definition on purpose. It is left upto the student to define any requierd arguments.
        Please change the signature of the function and add the arguments based on your implementation.
        
        The function ideally takes two 1D points Pt1 and Pt2, and their intensitites I(Pt1), I(Pt2).
        return the interpolated intensity value (I(x)) at location x """

        # Write your code for linear interpolation here
        if (Pt1 == Pt2):
            return I_Pt1
        else:
            interpolated_intensity = (I_Pt1 * (Pt2 - x) / (Pt2 - Pt1)) + (I_Pt2 * (x - Pt1) / (Pt2 - Pt1))
            return interpolated_intensity

    def bilinear_interpolation(self, P, NW_point, I_NW, NE_point, I_NE, SW_point, I_SW, SE_point, I_SE):
        """Computes the bilinear interpolation value at some 2D location x between four 2D points (Pt1, Pt2, Pt3, and Pt4).
        
        There are no arguments defined in the function definition on purpose. It is left upto the student to define any requierd arguments.
        Please change the signature of the function and add the arguments based on your implementation.
        
        The function ideally takes four 2D points Pt1, Pt2, Pt3, and Pt4, and their intensitites I(Pt1), I(Pt2), I(Pt3), and I(Pt4).
        return the interpolated intensity value (I(x)) at location x """

        # Write your code for bilinear interpolation here
        # Recall that bilinear interpolation performs linear interpolation three times
        # Please reuse or call linear interpolation method three times by passing the appropriate parameters to compute this task

        """
            NW   NE
               P
            SW   SE
            Points needed to calculate
            
            Then use linear_interpolation() to calculate the interpolation 3 times as in the slides.
        """

        top_bar = interpolation.linear_interpolation(self, P[0], NW_point[0], I_NW, NE_point[0], I_NE)
        bottom_bar = interpolation.linear_interpolation(self, P[0], SW_point[0], I_SW, SE_point[0], I_SE)
        interpolated_intensities = interpolation.linear_interpolation(self, P[1], NW_point[1], top_bar, SW_point[1], bottom_bar)

        return interpolated_intensities# An array containing the pixel values
