

export const getSession = async () => {
    try {
        const res = await fetch("/api/getsession", {
            credentials: "same-origin",
        });
        const data = await res.json();
        return data.login;
    } catch (err) {
        console.log(err);
        return false
    }
}

export const validatecsrf = async (csrfToken: string) => {
    try {
        const res = await fetch("/api/validatecsrf", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            credentials: "same-origin",
        });
        const data = await res.json();
        console.log(data);
        if (data.valid == true) {
            return true;
        } else {
            return false;
        }
    }catch (err) {
        console.log(err);
        return false;
    }
}

export const getCsrf = async () => {
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


export const signup = async (csrfToken: string, firstName: string, lastName: string, userEmail: string, password: string) => {
    try {
        const res = await fetch('/api/signup', {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                firstName,
                lastName,
                userEmail,
                password
            })
        });
        const data = await res.json();
        console.log("Signup response:" + data);
        return data;
    } catch (err) {
        console.log(err);
    }
};

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
        if (data.login == true) {
            return data;
        } else {
            return false;
        }
    } catch (err) {
        console.log(err);
        return false;
    }
}

export const logout = async ( ) => {
    try {
        const res = await fetch("/api/logout", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
            credentials: "same-origin",
        })
        const data = await res.json();
        return data;
    } catch (err) {
        console.log(err);
    }
}
