const API_BASE_URL = "http://103.151.63.84:8006/api";

async function requestAPI(
    endpoint,
    method = "GET",
    bodyData = null
) {

    const headers = {
        "Content-Type": "application/json"
    };

    const accessToken =
        localStorage.getItem(
            "access_token"
        );

    if(accessToken){

        headers["Authorization"] =
            `Bearer ${accessToken}`;
    }

    const options = {
        method,
        headers
    };

    if(bodyData){

        options.body =
            JSON.stringify(bodyData);
    }

    try{

        const response =
            await fetch(
                `${API_BASE_URL}${endpoint}`,
                options
            );

        const data =
            await response
                .json()
                .catch(() => null);

        return {

            ok: response.ok,

            status: response.status,

            data

        };

    }catch(error){

        console.error(
            "API Error:",
            error
        );

        return {

            ok: false,

            status: 500,

            data: null

        };
    }
}