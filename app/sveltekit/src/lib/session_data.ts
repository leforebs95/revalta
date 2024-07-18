

export const getSession = async () => {
    try {
        const res = await fetch("/api/getsession", {
            credentials: "same-origin",
        });
        const data = await res.json();
        console.log(data);
        if (data.login == true) {
            return true;
        } else {
            return false;
        }
    } catch (err) {
        console.log(err);
        return false
    }
}

export const csrf = async () => {
    try {
        const res = await fetch("/api/getcsrf", {
            credentials: "same-origin",
        });
        const csrfToken = res.headers.get("X-CSRFToken");
        return csrfToken;
    } catch (err) {
        console.log(err);
        return null
    }
}

export const login = async (csrfToken: string, userEmail: string, password: string) => {
    try {
        const res = await fetch("/api/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            credentials: "same-origin",
            body: JSON.stringify({ userEmail: userEmail, password: password }),
        });
        const data = await res.json();
        console.log(data);
        if (data.login == true) {
            return true;
        } else {
            return false;
        }
    } catch (err) {
        console.log(err);
        return false;
    }
}
