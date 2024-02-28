import React, { useState, useEffect } from 'react';
import Form from './component/Form';
import UserBox from './component/UserBox';

const App = () => {
  const [posts, setPosts] = useState([]);
  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/info/')
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        setPosts(data);
      })
      .catch((err) => {
        console.log(err.message);
      });
  }, []);

  const deletePost = async (id) => {
    try {
      let response = await fetch(`http://127.0.0.1:8000/api/info/${id}/`, {
        method: 'DELETE',
      });

      if (response.ok) {
        setPosts(
          posts.filter((post) => {
            return post.id !== id;
          })
        );
      } else {
        console.error(`Failed to delete post with ID ${id}`);
      }
    } catch (error) {
      console.error('Error deleting post:', error);
    }
  };


  const updatePost = async (id, newName, newEmail, newPassword, newDegree) => {
    try {
      let response = await fetch(`http://127.0.0.1:8000/api/info/${id}/`, {
        method: 'PUT',
        body: JSON.stringify({
          name: newName,
          email: newEmail,
          password: newPassword,
          degree: newDegree,
        }),
        headers: {
          'Content-type': 'application/json; charset=UTF-8',
        },
      });

      if (response.ok) {
        setPosts(
          posts.map((post) => {
            if (id === post.id) {
              return {
                ...post,
                name: newName,
                email: newEmail,
                password: newPassword,
                degree: newDegree,
              };
            }
            return post;
          })
        );
      } else {
        const errorData = await response.json();
        console.error('Error updating post:', errorData);
      }
    } catch (error) {
      console.error('Error updating post:', error);
    }
  };

  const addPosts = async (name, email, password, degree) => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/info/', {
        method: 'POST',
        body: JSON.stringify({
          name: name,
          email: email,
          password : password,
          degree : degree,
        }),
        headers: {
          'Content-type': 'application/json; charset=UTF-8',
        },
      });
      if (response.ok) {
        const data = await response.json();
        setPosts((posts) => [data, ...posts]);
      } else {
        const errorData = await response.json();
        console.error('Error updating post:', errorData);
      }
    } catch (err) {
      console.log(err.message);
    }
  };

    const postList = posts.map((post) => (
      <UserBox
        id={post.id}
        name={post.name}
        email={post.email}
        password={post.password}
        degree={post.degree}
        key={post.id}
        updatePost={updatePost}
        deletePost={deletePost}
      />
    ));

    const postNoun = postList.length > 0 ? "User" : "Users";
    const headingText = `${postList.length} ${postNoun} added!`;

    return (
      <div className="todoapp stack-large">
        <Form addPosts={addPosts} />
        <div className="filters btn-group stack-exception">{ }</div>
        <h2 id="list-heading" tabIndex="-1">
          {headingText}
        </h2>
        <ul
          className="todo-list stack-large stack-exception"
          aria-labelledby="list-heading">
          {postList}
        </ul>
      </div>
    );
  };

export default App;