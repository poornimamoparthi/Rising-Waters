// Front-end enhancements for the Flood Prediction form
document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('.predict-form');
    if (form) {
        // Form validations
        form.addEventListener('submit', (e) => {
            const annualRainfall = parseFloat(document.getElementById('Annual_Rainfall').value);
            const seasonalRainfall = parseFloat(document.getElementById('Seasonal_Rainfall').value);
            
            // Warnings
            if (seasonalRainfall > annualRainfall) {
                alert('Warning: Seasonal Rainfall should not exceed Annual Rainfall. Please check your inputs.');
                e.preventDefault();
                return;
            }
            
            const inputs = form.querySelectorAll('input[type="number"]');
            let hasError = false;
            inputs.forEach(input => {
                const val = parseFloat(input.value);
                const min = parseFloat(input.getAttribute('min'));
                const max = parseFloat(input.getAttribute('max'));
                
                if (isNaN(val)) {
                    alert(`${input.previousElementSibling.textContent} is required.`);
                    hasError = true;
                    e.preventDefault();
                } else if (min !== null && val < min) {
                    alert(`${input.previousElementSibling.textContent} must be at least ${min}.`);
                    hasError = true;
                    e.preventDefault();
                } else if (max !== null && val > max) {
                    alert(`${input.previousElementSibling.textContent} must be at most ${max}.`);
                    hasError = true;
                    e.preventDefault();
                }
            });
        });
    }
});
