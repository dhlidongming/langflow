import React, {useEffect} from 'react';
import {useLocation, useNavigate} from 'react-router-dom';
import {AuthContext} from "../../contexts/authContext";
import {useContext, useState} from "react";
import {useRefreshAccessToken} from "@queries/auth";
import {api} from "@/controllers/API/api";
import {getURL} from "@/controllers/API/helpers/constants";


// const CAS_SERVER_URL = 'https://sso.eos.dhgate.com/cas';
// const CAS_SERVER_URL = 'http://127.0.0.1:8000/cas/dhgate/application_python_example';
const CAS_SERVER_URL = 'http://172.21.80.24/cas';
const SERVICE_URL = '/sso_callback';

export function SSOLogin() {
    useEffect(() => {
        window.location.href = `${CAS_SERVER_URL}/login?service=${encodeURIComponent(`${window.location.origin}${SERVICE_URL}`)}`;
    }, []);

    return (
        <></>
    );
}

export const SSOCallback = () => {
    const {login} = useContext(AuthContext);
    const location = useLocation();
    const navigate = useNavigate(); // 使用 useNavigate 钩子

    const sso_login = () => {
        const urlParams = new URLSearchParams(location.search);
        const ticket = urlParams.get('ticket');

        if (ticket) {
            api.post(`${getURL("LOGIN")}?ticket=${ticket}&service_url=${window.location.origin}${SERVICE_URL}`).then(res => res.data).then((res) => {
                if (res.status === 'ok') {
                    console.log('Login success');
                    login(res.data.access_token, "login", res.data.refresh_token);
                    navigate("/all")
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
        <></>
    );
};