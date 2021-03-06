//--------------------------- VERSION 2 -----------------------------------//
import React from 'react';
// if you want to import something specific you will need to de-structure it using {}.
import { render } from 'react-dom';
// A provider that is Chakra UI needs. It is a requirment by Chakra UI
import { ChakraProvider } from '@chakra-ui/react';
// To provide redux to all our components
import { Provider } from 'react-redux';
// we will provide store as a property on Provider
import store from './store';
import App from './App';

render(
    // React.StrictMode:- is a new feature which is going to help us reduce errors.
    // It will essentially throw error back rather than stopping the entire app.

    // ChakraProvider:- This is a special requirement that is needed by Chakra.
    // Many such Component libraries have their own Providers. They essentially provide
    // some special functionalities to your existing components hence they are needed.

    // We dont need StrictMode anymore. It doesnt help us all that much
    // It just helps us know if we've added something unecessary or about errors,etc.
  <Provider store={store}>
    <ChakraProvider>
      <App />
    </ChakraProvider>
  </Provider>,
  document.querySelector('#root')
);

// In index.html there is a div inside our body tag. We want to render our entire
// page within that div, hence we do document.querySelector('#root').









// //--------------------------- VERSION 1 -----------------------------------//
// import React from 'react';
// // if you want to import something specific you will need to de-structure it using {}.
// import {render} from 'react-dom';
// import App from './App';

// // A provider that is Chakra UI needs. It is a requirment by Chakra UI
// import {ChakraProvider} from '@chakra-ui/react';

// render( 
//     // React.StrictMode:- is a new feature which is going to help us reduce errors.
//     // It will essentially throw error back rather than stopping the entire app.

//     // ChakraProvider:- This is a special requirement that is needed by Chakra.
//     // Many such Component libraries have their own Providers. They essentially provide
//     // some special functionalities to your existing components hence they are needed.
//     <React.StrictMode>
//         <ChakraProvider>
//             <App /> 
//         </ChakraProvider>
//     </React.StrictMode>
// , document.querySelector('#root'));

// // apne index.html mein there is a div inside our body tag. We want to render our entire
// // page within that div, hence we do document.querySelector('#root').






