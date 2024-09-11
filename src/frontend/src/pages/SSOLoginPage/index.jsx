import React, {useEffect} from 'react';

// const CAS_SERVER_URL = 'https://sso.eos.dhgate.com/cas';
// const CAS_SERVER_URL = 'http://127.0.0.1:8000/cas/dhgate/application_python_example';
const CAS_SERVER_URL = 'http://172.21.80.24/cas';
const SERVICE_URL = 'http://localhost:7860/callback';
const BACKEND_SERVICE_URL = 'http://127.0.0.1:7860/api/v1/login';

export function SSOLogin() {
    useEffect(() => {
        // window.location.href = window.sdk.getSigninUrl();
        window.location.href = `${CAS_SERVER_URL}/login?service=${encodeURIComponent(SERVICE_URL)}`;
    }, []);

    return (
        <div/>
    );
}

import {useLocation, useNavigate} from 'react-router-dom';
import {AuthContext} from "../../contexts/authContext";
import {useContext, useState} from "react";
import {useRefreshAccessToken} from "@queries/auth";


export const SSOCallback = () => {
    const {login} = useContext(AuthContext);
    const { mutate: mutateRefresh } = useRefreshAccessToken();

    const location = useLocation();
    const navigate = useNavigate(); // 使用 useNavigate 钩子

    const sso_login = () => {
        const urlParams = new URLSearchParams(location.search);
        const ticket = urlParams.get('ticket');

        if (ticket) {
            fetch(`${BACKEND_SERVICE_URL}?ticket=${ticket}`, {
                method: "POST",
                // credentials: "include",
            }).then(res => res.json()).then((res) => {
                if (res.status === 'ok') {
                    console.log('Login success');
                    login(res.data.access_token, "login", res.data.refresh_token);
                    navigate("/all")

                    // mutateRefresh();
                    // window.location.replace('/all');
                } else {
                    navigate('/login');
                }
            });
        } else {
            console.log('no ticket');
        }
    };

    useEffect(() => {
        sso_login();
    }, [location.search]);

    return (
        <div/>
    );
};


export function SSOCallbackCasdoor() {
    const {login} = useContext(AuthContext);

    const sso_login = () => {
        window.sdk.signin(ServerUrl).then((res) => {
            if (res.status === 'ok') {
                login(res.data.access_token, "login", res.data.refresh_token);
                console.log('Login success');
                window.location.replace('/');
            }
        });
    };

    useEffect(() => {
        sso_login();
    }, []);

    return (
        <div/>
    );
}