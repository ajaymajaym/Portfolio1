(function () {
    'use strict';

    const form = document.getElementById('contactForm');
    if (!form) return;

    const alertBox = document.getElementById('formAlert');
    const submitBtn = document.getElementById('submitBtn');
    const submitBtnText = document.getElementById('submitBtnText');
    const submitBtnSpinner = document.getElementById('submitBtnSpinner');

    function getCookie(name) {
        const match = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
        return match ? decodeURIComponent(match.pop()) : '';
    }

    function showAlert(type, message) {
        alertBox.className = 'alert alert-' + type;
        alertBox.textContent = message;
        alertBox.classList.remove('d-none');
    }

    function clearFieldErrors() {
        document.querySelectorAll('.invalid-feedback-custom').forEach((el) => (el.textContent = ''));
        document.querySelectorAll('.contact-card .form-control').forEach((el) => el.classList.remove('is-invalid'));
    }

    function showFieldErrors(errors) {
        Object.keys(errors).forEach((field) => {
            const target = document.querySelector('.invalid-feedback-custom[data-field="' + field + '"]');
            const input = document.getElementById('id_' + field);
            if (target) target.textContent = errors[field][0].message || errors[field][0];
            if (input) input.classList.add('is-invalid');
        });
    }

    function setLoading(isLoading) {
        submitBtn.disabled = isLoading;
        submitBtnText.classList.toggle('d-none', isLoading);
        submitBtnSpinner.classList.toggle('d-none', !isLoading);
    }

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        clearFieldErrors();
        alertBox.classList.add('d-none');
        setLoading(true);

        const formData = new FormData(form);

        fetch(form.action, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: formData,
        })
            .then((response) => response.json().then((data) => ({ status: response.status, data })))
            .then(({ status, data }) => {
                setLoading(false);
                if (data.success) {
                    showAlert('success', data.message || 'Your message has been sent successfully!');
                    form.reset();
                } else if (data.errors) {
                    showFieldErrors(data.errors);
                    showAlert('danger', 'Please fix the errors below and try again.');
                } else {
                    showAlert('danger', data.message || 'Something went wrong. Please try again.');
                }
            })
            .catch(() => {
                setLoading(false);
                showAlert('danger', 'Network error — please check your connection and try again.');
            });
    });
})();
