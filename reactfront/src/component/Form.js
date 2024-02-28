import React, { useState } from "react";

function Form(props) {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [degree, setDegree] = useState('');

    function handleSubmit(e) {
        e.preventDefault();
        if (!name.trim()) {
            return;
        }
        props.addPosts(name, email, password, degree);
        setName("");
        setEmail("");
        setPassword("");
        setDegree("");
    }

    return (
        <form onSubmit={handleSubmit}>
            <h2 className="label-wrapper">
                <label htmlFor="new-todo-input" className="label__lg">
                    Add New User
                </label>
            </h2>
            <label className="todo-label" htmlFor={props.id}>
            Name:
            </label>    
            <input
                type="text"
                id="new-todo-input"
                className="input input__lg"
                name="text"
                autoComplete="off"
                value={name}
                onChange={(e) => setName(e.target.value)}
            />
            <label className="todo-label" htmlFor={props.id}>
            Email:
            </label>
            <input
                type="text"
                id="new-todo-input"
                className="input input__lg"
                name="text"
                autoComplete="off"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
            />
            <label className="todo-label" htmlFor={props.id}>
            Password:
            </label>
            <input
                type="text"
                id="new-todo-input"
                className="input input__lg"
                name="text"
                autoComplete="off"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />
            <label className="todo-label" htmlFor={props.id}>
            Degree:
            </label>
            <input
                type="text"
                id="new-todo-input"
                className="input input__lg"
                name="text"
                autoComplete="off"
                value={degree}
                onChange={(e) => setDegree(e.target.value)}
            />
            <button type="submit" className="btn btn__primary btn__lg">
                Add
            </button>
        </form>
    );
}

export default Form;