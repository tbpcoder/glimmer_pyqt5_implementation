import cv2
import numpy as np
from PIL import ImageGrab
import screen_brightness_control as sbc
from typing import Tuple, Optional

class BrightnessController:
    """
    Controller for managing screen brightness based on ambient light conditions.
    
    This controller uses screen capture to determine ambient brightness and
    adjusts screen brightness accordingly, with support for manual overrides
    and configurable limits.
    """
    
    def __init__(self):
        """Initialize the brightness controller with default settings."""
        self.paused = False
        self.max_brightness_limit = 80  # Default maximum brightness
        self.min_brightness_limit = 20  # Default minimum brightness
        self.current_manual_brightness = None  # Store manual brightness setting
        self._last_captured_brightness = None  # Cache last captured brightness
        self._capture_error_count = 0  # Track consecutive capture errors
        
    def set_brightness_limits(self, max_brightness: int, min_brightness: int) -> None:
        """
        Set the maximum and minimum brightness limits.
        
        Args:
            max_brightness (int): Maximum allowed brightness (0-100)
            min_brightness (int): Minimum allowed brightness (0-100)
            
        Raises:
            ValueError: If brightness values are invalid or min > max
        """
        if not 0 <= min_brightness <= max_brightness <= 100:
            raise ValueError(
                "Invalid brightness limits. Must be: 0 <= min <= max <= 100"
            )
        
        self.max_brightness_limit = max_brightness
        self.min_brightness_limit = min_brightness
        
    def pause(self) -> None:
        """Pause automatic brightness adjustment."""
        self.paused = True
        
    def resume(self) -> None:
        """Resume automatic brightness adjustment."""
        self.paused = False
        self.current_manual_brightness = None  # Clear any manual brightness setting
        
    def get_average_brightness(self) -> Optional[float]:
        """
        Capture and calculate the average screen brightness.
        
        Returns:
            float or None: Average brightness value (0-255) or None if capture fails
            
        Notes:
            Uses screen capture to determine ambient brightness.
            Implements error handling and caching for reliability.
        """
        try:
            screen = ImageGrab.grab()  # Capture the entire screen
            screen_np = np.array(screen)
            frame = cv2.cvtColor(screen_np, cv2.COLOR_RGB2BGR)
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            avg_brightness = gray_frame.mean()
            
            self._last_captured_brightness = avg_brightness
            self._capture_error_count = 0  # Reset error count on successful capture
            return avg_brightness
            
        except Exception as e:
            self._capture_error_count += 1
            print(f"Error capturing screen (attempt {self._capture_error_count}): {e}")
            
            # Return last known good value if available and not too many errors
            if self._last_captured_brightness is not None and self._capture_error_count < 3:
                return self._last_captured_brightness
                
            return None
            
    def calculate_target_brightness(self, avg_brightness: float, sensitivity: float) -> Optional[float]:
        """
        Calculate target brightness based on ambient light and sensitivity.
        
        Args:
            avg_brightness (float): Average ambient brightness (0-255)
            sensitivity (float): Adjustment sensitivity factor
            
        Returns:
            float or None: Calculated target brightness (0-100) or None if calculation fails
            
        Notes:
            Higher sensitivity means stronger brightness adjustment response.
        """
        try:
            # Convert average brightness to a target screen brightness
            # As ambient light increases, screen brightness should decrease
            target = 1 - (avg_brightness * sensitivity / 2550)  # Normalized to 0-1
            return target * 100  # Convert to percentage
            
        except Exception as e:
            print(f"Error calculating target brightness: {e}")
            return None
            
    def adjust_brightness(self, sensitivity: float, max_brightness: int, 
                         min_brightness: int) -> Tuple[float, float]:
        """
        Adjust screen brightness based on ambient light and constraints.
        
        Args:
            sensitivity (float): Adjustment sensitivity (1-10)
            max_brightness (int): Maximum allowed brightness (0-100)
            min_brightness (int): Minimum allowed brightness (0-100)
            
        Returns:
            tuple: (average_brightness, target_brightness)
            - average_brightness (float): Measured ambient brightness
            - target_brightness (float): Applied screen brightness
            
        Notes:
            Returns (0, 0) if paused or if brightness adjustment fails.
        """
        if self.paused:
            return 0, 0

        # Get ambient brightness
        avg_brightness = self.get_average_brightness()
        if avg_brightness is None:
            return 0, 0
            
        # Calculate target brightness
        target_brightness = self.calculate_target_brightness(avg_brightness, sensitivity)
        if target_brightness is None:
            return 0, 0
            
        # Apply brightness limits
        target_brightness = min(max(target_brightness, min_brightness), max_brightness)
        
        try:
            sbc.set_brightness(int(target_brightness))
            return avg_brightness, target_brightness
            
        except Exception as e:
            print(f"Error setting brightness: {e}")
            return 0, 0
            
    def set_manual_brightness(self, brightness: int) -> None:
        """
        Manually set screen brightness to a specific value.
        
        Args:
            brightness (int): Target brightness level (0-100)
            
        Raises:
            ValueError: If brightness value is out of valid range
        """
        if not 0 <= brightness <= 100:
            raise ValueError("Brightness must be between 0 and 100")
            
        try:
            sbc.set_brightness(brightness)
            self.current_manual_brightness = brightness
        except Exception as e:
            print(f"Error setting manual brightness: {e}")
            
    def get_current_brightness(self) -> int:
        """
        Get the current screen brightness level.
        
        Returns:
            int: Current brightness level (0-100)
        """
        try:
            return sbc.get_brightness()[0]  # Returns first monitor's brightness
        except Exception as e:
            print(f"Error getting current brightness: {e}")
            return 0