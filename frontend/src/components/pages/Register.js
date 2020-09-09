import React, { useState, useContext } from "react";
import { useForm } from "react-hook-form";
import { Redirect } from "react-router-dom";

import { AppContext } from "components/pages/App";
import { register } from "services/auth";

const RegisterPage = () => {
  const {
    register: registerInput,
    handleSubmit,
    errors,
    setError: setValidationError,
  } = useForm();
  const [serverError, setServerError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const {
    state: { isLoggedIn },
    action,
  } = useContext(AppContext);

  if (isLoggedIn) return <Redirect to="/" />;

  const onSubmit = async (input) => {
    if (input.password !== input.confirmPassword)
      return setValidationError("confirmPassword", true);
    setIsLoading(true);
    const { data, error } = await register(input);
    setIsLoading(false);
    if (error) return setServerError(error);
    action("login", data);
  };

  return (
    <div className="register">
      <div className="column col-3 col-mx-auto card">
        <div className="card-body">
          <h2 className="text-center">Register</h2>
          <form onSubmit={handleSubmit(onSubmit)}>
            <div className={`form-group ${errors.username ? "has-error" : ""}`}>
              <label className="form-label" htmlFor="username">
                Username
              </label>
              <input
                className="form-input"
                type="text"
                id="username"
                name="username"
                placeholder="Username"
                ref={registerInput({
                  required: true,
                  minLength: 3,
                  maxLength: 30,
                })}
              />
              <span className="form-input-hint">
                {errors.username?.type === "required" && "Required"}
                {errors.username?.type === "minLength" &&
                  "Must be at least 5 chars"}
                {errors.username?.type === "maxLength" &&
                  "Must be less than 50 chars"}
              </span>
            </div>
            <div className={`form-group ${errors.password ? "has-error" : ""}`}>
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
                ref={registerInput({
                  required: true,
                  minLength: 5,
                  maxLength: 50,
                })}
              />
              <span className="form-input-hint">
                {errors.password?.type === "required" && "Required"}
                {errors.password?.type === "minLength" &&
                  "Must be at least 5 chars"}
                {errors.password?.type === "maxLength" &&
                  "Must be less than 50 chars"}
              </span>
            </div>
            <div
              className={`form-group ${
                errors.confirmPassword ? "has-error" : ""
              }`}
            >
              <label
                className="form-label"
                disabled={isLoading}
                htmlFor="confirm-password"
              >
                Confirm Password
              </label>
              <input
                className="form-input"
                type="password"
                id="confirm-password"
                name="confirmPassword"
                placeholder="Password"
                ref={registerInput}
              />
              <span className="form-input-hint">
                {errors.confirmPassword && "Does not match"}
              </span>
            </div>
            <div className="text-center text-error login-error">
              {serverError}
            </div>
            <button
              className={`btn btn-primary ${isLoading ? "loading" : ""}`}
              disabled={isLoading}
            >
              Login
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default RegisterPage;
