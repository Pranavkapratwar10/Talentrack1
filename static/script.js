// Toggle password visibility
function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    const icon = input.parentElement.querySelector('.toggle-password');
    
    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.add('active');
    } else {
        input.type = 'password';
        icon.classList.remove('active');
    }
}

// Password validation for registration form
document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.getElementById('registerForm');
    
    if (registerForm) {
        const passwordInput = document.getElementById('password');
        const confirmPasswordInput = document.getElementById('confirm_password');
        const passwordMatchMsg = document.getElementById('password-match');

        // Password strength validation
        passwordInput.addEventListener('input', function() {
            const password = this.value;
            
            // Check length
            const lengthRule = document.getElementById('rule-length');
            if (password.length >= 8) {
                lengthRule.classList.add('valid');
            } else {
                lengthRule.classList.remove('valid');
            }

            // Check uppercase
            const uppercaseRule = document.getElementById('rule-uppercase');
            if (/[A-Z]/.test(password)) {
                uppercaseRule.classList.add('valid');
            } else {
                uppercaseRule.classList.remove('valid');
            }

            // Check lowercase
            const lowercaseRule = document.getElementById('rule-lowercase');
            if (/[a-z]/.test(password)) {
                lowercaseRule.classList.add('valid');
            } else {
                lowercaseRule.classList.remove('valid');
            }

            // Check number
            const numberRule = document.getElementById('rule-number');
            if (/\d/.test(password)) {
                numberRule.classList.add('valid');
            } else {
                numberRule.classList.remove('valid');
            }

            // Check special character
            const specialRule = document.getElementById('rule-special');
            if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
                specialRule.classList.add('valid');
            } else {
                specialRule.classList.remove('valid');
            }

            // Check password match
            checkPasswordMatch();
        });

        // Confirm password validation
        confirmPasswordInput.addEventListener('input', checkPasswordMatch);

        function checkPasswordMatch() {
            const password = passwordInput.value;
            const confirmPassword = confirmPasswordInput.value;

            if (confirmPassword === '') {
                passwordMatchMsg.textContent = '';
                passwordMatchMsg.className = '';
                return;
            }

            if (password === confirmPassword) {
                passwordMatchMsg.textContent = '✓ Passwords match';
                passwordMatchMsg.className = 'valid';
            } else {
                passwordMatchMsg.textContent = '✗ Passwords do not match';
                passwordMatchMsg.className = 'invalid';
            }
        }

        // Form submission validation
        registerForm.addEventListener('submit', function(e) {
            const password = passwordInput.value;
            const confirmPassword = confirmPasswordInput.value;

            // Check all password rules
            const isLengthValid = password.length >= 8;
            const hasUppercase = /[A-Z]/.test(password);
            const hasLowercase = /[a-z]/.test(password);
            const hasNumber = /\d/.test(password);
            const hasSpecial = /[!@#$%^&*(),.?":{}|<>]/.test(password);

            if (!isLengthValid || !hasUppercase || !hasLowercase || !hasNumber || !hasSpecial) {
                e.preventDefault();
                alert('Please ensure your password meets all requirements');
                return false;
            }

            if (password !== confirmPassword) {
                e.preventDefault();
                alert('Passwords do not match');
                return false;
            }
        });
    }

    // Auto-hide flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.flash');
    flashMessages.forEach(function(flash) {
        setTimeout(function() {
            flash.style.opacity = '0';
            flash.style.transition = 'opacity 0.5s ease';
            setTimeout(function() {
                flash.remove();
            }, 500);
        }, 5000);
    });

    // Mobile number validation
    const mobileInput = document.getElementById('mobile');
    if (mobileInput) {
        mobileInput.addEventListener('input', function() {
            this.value = this.value.replace(/\D/g, '').slice(0, 10);
        });
    }
});


// View resume data toggle
function viewResumeData(resumeId) {
    const dataDiv = document.getElementById('resume-data-' + resumeId);
    if (dataDiv.style.display === 'none') {
        dataDiv.style.display = 'block';
    } else {
        dataDiv.style.display = 'none';
    }
}
