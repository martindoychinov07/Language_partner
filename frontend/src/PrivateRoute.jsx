import React, { useContext } from 'react';
import { Route, Navigate } from 'react-router-dom';
import { AuthContext } from './AuthContext';

const PrivateRoute = ({ element: Element, ...rest }) => {
  const { isAuthenticated } = useContext(AuthContext);

  return (
    <Route
      {...rest}
      element={
        isAuthenticated ? <Element /> : <Navigate to="/login" replace />
      }
    />
  );
};

export default PrivateRoute;
