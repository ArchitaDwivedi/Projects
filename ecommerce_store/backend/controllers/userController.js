import asyncHandler from 'express-async-handler';
import User from '../models/userModel.js';
import generateToken from '../utils/generateToken.js';



// First we will authenticate the user and then get the token.
// Obviously this is going to be a POST request.
// Our route will be /api/users/login.
// as this is the backend we can use our asyncHandler instead of try catch for our
// async request.
// ** Remember that whenever you do a POST request. The JSON response you get back will always be 
// found in the request object's body key.
const authUser = asyncHandler(async (req, res) => {
  // Get the data from the request body
  const { email, password } = req.body;

  const user = await User.findOne({ email });
  // if the user exists
  // we check if the the entered password is right
  // The comparing is going to take time, which is why in our userModel
  // if you see, our function is async. So we must await here for the function to respond.
  // (Or else we would have to use .then() which is something we dont want to do.)
  if (user && (await user.matchPassword(password))) {
    res.json({
      _id: user._id,
      name: user.name,
      email: user.email,
      isAdmin: user.isAdmin,
      // call generateToken function and pass the user's id
      // for payload.
      token: generateToken(user._id),
    });
  } else {
    // if user does not exist, then we'll just create a 401 (Unauthorized).
    res.status(401);
    throw new Error('Invalid email or password');
  }
});




const registerUser = asyncHandler(async (req, res) => {
  const { name, email, password } = req.body;

  // to check if user already exists!
  const userExists = await User.findOne({ email });

  if (userExists) {
    res.status(400); // Bad req
    throw new Error('User already exists');
  }

  const user = await User.create({ name, email, password });
  // Remember that our password is still not encryted!!
  if (user) {
    // 201 - something was successfully created
    res.status(201).json({
      _id: user._id,
      name: user.name,
      email: user.email,
      isAdmin: user.isAdmin,
// once the user registers succesfully, we'll immediately generate a token for
      // them, so they can login
      token: generateToken(user._id),
    });// succes: something was succefully created!
  } else {
    res.status(400); // Bad Req
    throw new Error('Invalid user data');
  }
});



const getUserProfile = asyncHandler(async (req, res) => {
  const user = await User.findById(req.user._id);

  if (user) {
    res.json({
      _id: user._id,
      name: user.name,
      email: user.email,
      isAdmin: user.isAdmin,
    });
  } else {
    res.status(404);
    throw new Error('User not found');
  }
});


// Updating user profile
const updateUserProfile = asyncHandler(async (req, res) => {
  //(*)user is MongoDB object
  const user = await User.findById(req.user._id);

  if (user) {
    // if name updated then change, else keep the same
    user.name = req.body.name || user.name;
    user.email = req.body.email || user.email;
// if req.body.passsword exists in the first place, only
    // then we update it. Else ignore it altogether.
    if (req.body.password) {
      user.password = req.body.password;
    }
// The save() function, is the one which actually goes and writes i.e updates
        // we will get the entire object back on saving.
        // make sure 'user' is a mongodb object(*)
    const updatedUser = await user.save();
    // Remember that our password is still not encryted!!
    res.json({
      _id: updatedUser._id,
      name: updatedUser.name,
      email: updatedUser.email,
      isAdmin: updatedUser.isAdmin,
      token: generateToken(updatedUser._id),
    });
  } else {
// if user does not exist, then we'll just create a 404.
        // (When we trhow an Error it will go to middleware which will convert it to JS
    res.status(404);
    throw new Error('User not found');
  }
});




// Admin side controller

// get all users
const getUsers = asyncHandler(async (req, res) => {
  const users = await User.find({});
  res.json(users);
});



const deleteUser = asyncHandler(async (req, res) => {
  const user = await User.findById(req.params.id);

  if (user) {
    // to delete
    await user.remove();
    res.json({ message: 'User deleted' });
  } else {
    res.status(404);
    throw new Error('User not found');
  }
});



// first get the pre-existing data before updating
const getUserById = asyncHandler(async (req, res) => {
  const user = await User.findById(req.params.id).select('-password');
  if (user) {
    res.json(user);
  } else {
    res.status(404);
    throw new Error('User not found');
  }
});


// to update
const updateUser = asyncHandler(async (req, res) => {
  const user = await User.findById(req.params.id);

  if (user) {
    user.name = req.body.name || user.name;
    user.email = req.body.email || user.email;
    user.isAdmin = req.body.isAdmin;

    const updatedUser = await user.save();

    res.json({
      _id: updateUser._id,
      name: updatedUser.name,
      email: updatedUser.email,
      isAdmin: updatedUser.isAdmin,
    });
  } else {
    res.status(404);
    throw new Error('User not found');
  }
});



export {
  authUser,
  getUserProfile,
  registerUser,
  updateUserProfile,
  getUsers,
  deleteUser,
  updateUser,
  getUserById,
};
