import os

from casdoor import CasdoorSDK
from cas import CASClient

certificate = '''-----BEGIN CERTIFICATE-----
MIIE3TCCAsWgAwIBAgIDAeJAMA0GCSqGSIb3DQEBCwUAMCgxDjAMBgNVBAoTBWFkbWluMRYwFAYDVQQDEw1jZXJ0LWJ1aWx0LWluMB4XDTI0MDkwOTA5MjQxMFoXDTQ0MDkwOTA5MjQxMFowKDEOMAwGA1UEChMFYWRtaW4xFjAUBgNVBAMTDWNlcnQtYnVpbHQtaW4wggIiMA0GCSqGSIb3DQEBAQUAA4ICDwAwggIKAoICAQDpMkfFUwiQgopRhbjcH54TjsX2vdAYEa3LmJ2TSxPssAgE/KmVCyQOwfmLZL469JXKIKAaKjj6UtVI2pbC1UcQ8GqALrdXSFun29aEmXXarHEwcVkc0JYMLH4oYC2Nj7p3aQ8Mpf44YQBE57TM+uJkHY3qih3xAP+nGYkE75ByqxQavLHbnxL/pEIueNlDd/5syBn7258qRTKvFM3Fv8IXIH8k7QZrT4AaWta/sdEMCdphaXr3AiEGDsLV0Wls10uWmWklvHLtirRKudixcHsP2kCJdiPjcZlmv7clXErXnnvipu8IGmcaXIQUqemt9ABjTaU2+kvkqw481HVWJEkq7wiDh4Qes81+KRnVqTbJR0I6LdG3NqdyaHMwK8DwFPnioYEpf8jBUUngSRESLomhVjxDiHYZJa5NGDL1M0GFuiIkP+xcnl311Zk0agoC6U17/GVRiVHGlILIZiJd2iXQC9Q/QBeqkWZ0bXfdv63m4sSKfavt2KN3wBf4JAfO/vgi3fhrKypy7bS0JdDUERQx8TP+n+LyvtVLXX4k8iMRkmtHczpA/2kTeP9cdOm5QRbiAu3wJmKJWyKAbCdl85T+NJFVaXcf3F4y6Es3ti3JiFS7KsZq+OxEaS7dbYkazbWQE1O02cj5aVpmjLEyFT3Qc3xMS1v5z5/UsL3wJHeVswIDAQABoxAwDjAMBgNVHRMBAf8EAjAAMA0GCSqGSIb3DQEBCwUAA4ICAQAM4uULRC26oB4qnEERm08OslQYrO/jtN2LW24aXtqiAJ3P0iNkwt/K1Gy5vYt1LUJImREe5CM5K4Zhr6447LyYRDEXzEuqx8p46jgtP0K8PMUDazgNIAJxICaExj0peq3LKvh7GiojX7Ws7ColGP2PkR80RHtNeqAmRZo1VP7+7coKiAhGZBJwECqEkQjD95ebb8JX54NZAAeV8iq5k+5c99QzOCQPH6R/LIx6DipcjRGZ2CLLhMmJvmVDRbq6KjKSgrHHk021W+RXzN/NBPKXne5wfjYJ69eN9TA/witk7gW7sjy38YtxBZ2Bu5/JAkFOGUq2SqaokDqF81w8x/ZvB+1FFnAeFNLMn1An5LKAa+tF65RG/5K44sSktYBB1vGu3bvs7fbgBpLuTZEPw3mPY2Qe3Nc809jYK3vku6yqDpqTuGctjMLY1VAtVO4eetF33EiZ4g6Iv+ew7x6uurvKtVv07pKJt7Q6NX4BzUScO45reCIR7rj3i/qF0pskYYfDAblKXu/hZ1JuJkhmAQUrFnJgyt/Qdkx2Ti0Ind2QFAXPO8Q/BqqW/0dmnTyxaUBLVhiI7ITfF8Znvzq/87Xb/lYsmdJIr1QK+qRTrZxONDgRsiQP4126aSL0vkR8Ee0G4keg8vQy5FBp1CVHUPxc3YLAyoD99PyLq9HE5NA85g==
-----END CERTIFICATE-----'''

class Config:
    # CASDOOR_SDK = CasdoorSDK(
    #     endpoint='http://127.0.0.1:8000',
    #     client_id='3a278c0c55e5918cc6b6',
    #     client_secret='297b634dc8df16c1464c6801311dc2aad7254d8b',
    #     certificate=certificate,
    #     org_name='dhgate',
    #     application_name='application_python_example',
    # )
    # SECRET_TYPE = 'filesystem'
    # SECRET_KEY = os.urandom(24)

    cas_client = CASClient(
        version=3,
        service_url='http://localhost:7860/callback',
        # server_url='https://sso.eos.dhgate.com/cas',
        # server_url='http://127.0.0.1:8000/cas/dhgate/application_python_example',
        server_url='http://172.21.80.24/cas',
    )