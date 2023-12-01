import { Link } from "react-router-dom";
import React from "react";
import * as bases from "../components/ui/bases";
import _default from "react-redux/es/components/connect";

export default function Login() {
    return(   
          <div className="form-signin w-100 m-auto">
            <form>
              <img className="mb-4" src="public/logo192.png" alt="" width="72" height="57"/>
              <h1 className="h3 mb-3 fw-normal">Please sign in</h1>
              <div className="form-floating">
                <input type="email" className="form-control" id="floatingInput" placeholder="name@example.com"/>
                <label htmlFor="floatingInput">Email address</label>
              </div>
              <div className="form-floating">
                <input type="password" className="form-control" id="floatingPassword" placeholder="Password"/>
                <label htmlFor="floatingPassword">Password</label>
              </div>

              <div className="form-check text-start my-3">
                <input className="form-check-input" type="checkbox" value="remember-me" id="flexCheckDefault"/>
                <label className="form-check-label" htmlFor="flexCheckDefault">
                  Remember me
                </label>
              </div>
              <button className="btn btn-primary w-100 py-2" type="submit">Sign in</button>
              <p className="mt-5 mb-3 text-body-secondary">© 2017–2023</p>
            </form>
          </div>
    )
}
