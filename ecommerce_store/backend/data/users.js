import bcrypt from 'bcryptjs';

// We're using bcrypt for temporary use
// Hashing our password
const users = [
  {
    name: 'Administrator',
    email: 'email@example.com',
    password: bcrypt.hashSync('123456', 10),
    isAdmin: true,
  },
  {
    name: 'John Doe',
    email: 'john@example.com',
    password: bcrypt.hashSync('123456', 10),
  },
  {
    name: 'Jane Doe',
    email: 'jane@example.com',
    password: bcrypt.hashSync('123456', 10),
  },
];

export default users;
