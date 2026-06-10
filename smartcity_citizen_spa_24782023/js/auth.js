function setupLoginForm() {
    const form = document.getElementById("login-form");

    if (!form) {
        console.log("Form login tidak ditemukan");
        return;
    }

    form.addEventListener("submit", async function (event) {
        event.preventDefault();

        const username =
            document.getElementById("loginUsername").value;

        const password =
            document.getElementById("loginPassword").value;

        const result = await requestAPI(
            "/token/",
            "POST",
            {
                username,
                password
            }
        );

        console.log("Response Login:", result);

        if (result.status === 200) {

            localStorage.setItem(
                "access_token",
                result.data.access
            );

            localStorage.setItem(
                "refresh_token",
                result.data.refresh
            );

            localStorage.setItem(
                "username",
                username
            );

            console.log(
                "Username tersimpan:",
                localStorage.getItem("username")
            );

            alert("Login berhasil!");

            window.location.hash = "#dashboard";

        } else {

            alert(
                "Login gagal. Periksa username dan password."
            );
        }
    });
}

function logout() {

    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("username");

    alert("Logout berhasil!");

    window.location.hash = "#login";
}