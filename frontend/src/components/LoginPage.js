import React, { useState, useContext } from "react";
import { Redirect } from "react-router-dom";
import { useForm } from "react-hook-form";

import login from "../services/login";
import { AppContext } from "./App";

function LoginPage() {
  const { register, handleSubmit } = useForm();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const { state, setState } = useContext(AppContext);

  if (state.isLoggedIn) return <Redirect to="/" />;

  const onSubmit = async (input) => {
    setIsLoading(true);
    const { data, error } = await login(input);
    setIsLoading(false);
    if (error) return setError(error);
    setState({ isLoggedIn: true, username: data });
  };

  return (
    <div className="login">
      <div className="column col-3 col-mx-auto card">
        <div className="card-body">
          <h2 className="text-center">Login</h2>
          <form onSubmit={handleSubmit(onSubmit)}>
            <label className="form-label" htmlFor="username">
              Username
            </label>
            <input
              className="form-input"
              type="text"
              id="username"
              name="username"
              placeholder="Username"
              ref={register}
              required
            />
            <label
              className="form-label"
              disabled={isLoading}
              htmlFor="password"
            >
              Password
            </label>
            <input
              className="form-input"
              type="password"
              id="password"
              name="password"
              placeholder="Password"
              ref={register}
              required
            />
            <div className="text-center text-error login-error">{error}</div>
            <div className="text-center auth-btn">
              <button
                className={`btn btn-primary ${isLoading ? "loading" : ""}`}
                disabled={isLoading}
              >
                Login
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default LoginPage;
