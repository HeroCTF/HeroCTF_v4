function generateRandomString() {
    var result           = '';
    var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for ( var i = 0; i < 15; i++ ) {
      result += characters.charAt(Math.floor(Math.random() * 
 charactersLength));
   }
   return result;
}

async function canAccessForm(usersModel, req)
{
  if(req.session.name !== undefined)
  {
      let possibleUser,err;
      await usersModel.selectUser(req.session.name).then((resp) => {possibleUser = resp}).catch((resp) => {err = resp})
      if(err)
      {
          return false;
      }else
      {
          if(possibleUser.length > 0)
          {
              if(possibleUser[0]['canAccessForm'] === 1) return true
              else return false;
          }else return false;
      }
  }else return false;
}

module.exports = {generateRandomString, canAccessForm}