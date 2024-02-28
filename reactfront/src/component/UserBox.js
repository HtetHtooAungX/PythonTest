import React, { useEffect, useRef, useState } from "react";


function usePrevious(value) {
    const ref = useRef();
    useEffect(() => {
        ref.current = value;
    });
    return ref.current;
}

export default function UserBox(props) {
    const [isEditing, setEditing] = useState(false);
    const [newName, setNewName] = useState(props.name);
    const [newEmail, setNewEmail] = useState(props.email);
    const [newPassword, setNewPassword] = useState(props.password);
    const [newDegree, setNewDegree] = useState(props.degree);

    const editFieldRef = useRef(null);
    const editButtonRef = useRef(null);

    const wasEditing = usePrevious(isEditing);

    function handleSubmit(e) {
        e.preventDefault();
        if (!newName.trim()) {
            return;
        }
        props.updatePost(props.id, newName, newEmail, newPassword, newDegree);
        setNewName("");
        setNewEmail("");
        setNewPassword("");
        setNewDegree("");
        setEditing(false);
    }

    const editingTemplate = (
        <form className="stack-small" onSubmit={handleSubmit}>
            <div className="form-group">
                <label className="todo-label" htmlFor={props.id}>
                    New name for {props.name}
                </label>
                <input
                    id={props.id}
                    className="todo-text"
                    type="text"
                    value={newName || props.name}
                    onChange={(e) => setNewName(e.target.value)}
                    ref={editFieldRef}
                />
                <label className="todo-label" htmlFor={props.id}>
                    New Email for {props.name}
                </label>
                <input
                    id={props.id}
                    className="todo-text"
                    type="text"
                    value={newEmail || props.email}
                    onChange={(e) => setNewEmail(e.target.value)}
                    ref={editFieldRef}
                />
                <label className="todo-label" htmlFor={props.id}>
                    New Password for {props.name}
                </label>
                <input
                    id={props.id}
                    className="todo-text"
                    type="text"
                    value={newPassword || props.password}
                    onChange={(e) => setNewPassword(e.target.value)}
                    ref={editFieldRef}
                />
                <label className="todo-label" htmlFor={props.id}>
                    New Degree for {props.name}
                </label>
                <input
                    id={props.id}
                    className="todo-text"
                    type="text"
                    value={newDegree || props.degree}
                    onChange={(e) => setNewDegree(e.target.value)}
                    ref={editFieldRef}
                />
            </div>
            <div className="btn-group">

                <button
                    type="button"
                    className="btn todo-cancel"
                    onClick={() => setEditing(false)}
                >
                    Cancel
                    <span className="visually-hidden">renaming {props.name}</span>
                </button>
                <button type="submit" className="btn btn__primary todo-edit">
                    Save
                    <span className="visually-hidden">new name for {props.name}</span>
                </button>
            </div>
        </form>
    );

    const viewTemplate = (
        <div className="stack-small">
            <div className="todo">
                <label className="todo-label" htmlFor={props.id}>
                    {props.name}
                </label>
                <label className="todo-label" htmlFor={props.id}>
                    {props.email}
                </label>
                <label className="todo-label" htmlFor={props.id}>
                    {props.degree}
                </label>
            </div>
            <div className="btn-group">
                <button
                    type="button"
                    className="btn"
                    onClick={() => setEditing(true)}
                    ref={editButtonRef}
                >
                    Edit <span className="visually-hidden">{props.name}</span>
                </button>
                <button
                    type="button"
                    className="btn btn__danger"
                    onClick={() => props.deletePost(props.id)}
                >
                    Delete <span className="visually-hidden">{props.name}</span>
                </button>
            </div>
        </div>
    );


    useEffect(() => {
        if (!wasEditing && isEditing) {
            editFieldRef.current.focus();
        }
        if (wasEditing && !isEditing) {
            editButtonRef.current.focus();
        }
    }, [wasEditing, isEditing]);


    return <li className="todo">{isEditing ? editingTemplate : viewTemplate}</li>;
}