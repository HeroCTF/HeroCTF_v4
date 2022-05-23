const { Sequelize, Model, DataTypes } = require('sequelize');
const sequelize = new Sequelize({
    dialect: "sqlite",
    storage: "presales.sqlite3"
});

class Users extends Model{}
Users.init({
    alias: {
        type: DataTypes.STRING,
        primaryKey: true
    },
    password: {
        type: DataTypes.STRING
    },
    canAccessForm: {
        type: DataTypes.INTEGER
    }
},
{
    sequelize: sequelize,
    modelName: 'users',
    timestamps: false,
    createdAt: false,
    updatedAt: false
})

let insertUser = async function(alias,pwd)
{
    await Users.create({
        alias: alias,
        password: pwd
    })
    return true;
}

let selectUser = async function(alias)
{
    return await Users.findAll({
        where: {
            alias: alias
        }
    })
}

let updateUser = async function(alias)
{
    return await Users.update(
    {
        canAccessForm: 1,
    },
    {
        where: {
            alias: alias
        }
    })
}


module.exports = {
    insertUser,
    selectUser,
    updateUser
}