function submitForm() {
	const formData = this.formData;

	fetch("/auth/register", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify(formData),
	})
		.then((response) => {
			// Handle the response
			if (response.ok) {
				// Handle successful response
				console.log("Form submitted successfully");
				window.location.href = "/login";
			} else {
				// Handle error response
				console.error("Error submitting form");
			}
		})
		.catch((error) => {
			// Handle network or other errors
			console.error("An error occurred", error);
		});
}
