import React, {useEffect, useState} from 'react';
import './App.css';
import axios from "axios";


export default function App() {
  const [token, setToken] = useState("");
  const [authState, setAuthState] = useState(false);
  const [profiledata, setData] = useState({data:{}});
  const [errorState, setErrorState] = useState(false)
  let username = "";
  let password = "";

  async function loginUser(){
      const response = await axios.post("http://127.0.0.1:8000/api/token/", {
      username: username, password: password
        }).then((response) => { // @ts-ignore
          setToken(response?.data.access);
          setAuthState(true);
        }).catch((error) => {
            setErrorState(true);
      })
  }

  async function getData(){
      const request = await axios.get('http://127.0.0.1:8000/api/debug/', {headers: {Authorization: `Bearer ${token}`}}).then(
          (request) =>
          {
              setData({data: request?.data});
              console.log(request?.data)
          });

  }



useEffect(() => {getData().catch((error) => {})}, [authState]);


    return (<div>
        {authState && (<div className="my-5">
            <div className="p-5 text-center bg-body-tertiary">
                <div className="container py-5">
                    <h1 className="text-body-emphasis">Профиль {
                        // @ts-ignore
                        profiledata.data.username
                    }</h1>
                    <p className="col-lg-8 mx-auto lead">
                        Дата регистрации: {
                        // @ts-ignore
                        new Date(profiledata.data.date_joined).toString().slice(3, 16)
                    }
                    </p>
                    <p className="col-lg-8 mx-auto lead">
                        Имя:
                        {
                            // @ts-ignore
                            profiledata.data.first_name
                        }
                    </p>
                    <p className="col-lg-8 mx-auto lead">
                        Фамилия:
                        {
                            // @ts-ignore
                            profiledata.data.last_name
                        }
                    </p>
                    <p className="col-lg-8 mx-auto lead">
                        Статус персонала:
                        {
                            // @ts-ignore
                            profiledata.data.is_staff ? ('Да') : ('Нет')
                        }
                    </p>
                    <button className="btn btn-primary mb-1" type="button" data-bs-toggle="collapse"
                            data-bs-target="#collapseExample" aria-expanded="false" aria-controls="collapseExample">
                        Конфиденциальная информация
                    </button>
                    <div className="collapse" id="collapseExample">
                        <div className="card card-body">
                            Айди пользователя: {
                            // @ts-ignore
                            profiledata.data.id
                        }
                        <br/>
                            Зашифрованный пароль: {
                            // @ts-ignore
                            profiledata.data.password
                        }
                        </div>
                    </div>
            </div>
            </div>
            </div>
        )}
        {!authState && (<div className="form-signin w-100 m-auto" id={'m'}>
            <div>{errorState && (<div className={'text-bg-danger text-center py-2 fw-bolder rounded py-1'}>Что-то пошло не так. <br/> Попробуйте еще раз</div>)}</div>
            <form className={'mb-1'} id={'f'} onSubmit={
                (event) => {
                    event.preventDefault();
                    loginUser();
                }}>
                <h1 className="h3 mb-3 fw-normal">Подтвердите свою личность</h1>
                <div className="form-floating mb-1"><input type="text" className="form-control" id="floatingInput" placeholder="name@example.com" onChange={
                    (event) => {
                        username = event.target.value;
                    }}/>
                    <label htmlFor="floatingInput">Email</label>
                </div>
                <div className="form-floating mb-1"><input type="password" className="form-control" id="floatingPassword" placeholder="Password" onChange={
                    (event) => {
                        password = event.target.value;
                    }}/>
                    <label htmlFor="floatingPassword">Пароль</label>
                </div>
                <button className="btn btn-primary w-100 py-2" type="submit">Войти</button>
                <p className="mt-5 mb-3 text-body-secondary">© 2024</p>
            </form>
        </div>
        )}
        </div>);
}


