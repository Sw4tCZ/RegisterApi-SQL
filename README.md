# RegisterApi-SQL
![Main image](https://github.com/Sw4tCZ/RegisterApi-SQL/blob/main/API1.png)

Tato webová aplikace je navržena v angličtině tak, aby uživatelům umožnila spravovat své dovednosti. Aplikace obsahuje následující funkce:

- Přihlášení a registrace uživatelů: Aplikace umožňuje uživatelům se registrovat a přihlašovat pomocí jména uživetele a hesla. 
  Po úspěšném přihlášení získá uživatel přístup k ovládacímu panelu (dashboard). V SQL databázi je navíc heslo zašifrované pomocí werkzeug-hash.
<p align="center">
  <img src="https://github.com/Sw4tCZ/RegisterApi-SQL/blob/main/API2.png" width="45%" />
  <img src="https://github.com/Sw4tCZ/RegisterApi-SQL/blob/main/API3.png" width="45%" /> 
</p>

- Dashboard: Na ovládacím panelu mohou uživatelé spravovat své dovednosti. 
  Mohou přidávat, upravovat a odebírat dovednosti ze seznamu. Seznam dovedností je reprezentován nečíslovaným seznamem a každá dovednost je zobrazena jako       položka seznamu spolu s tlačítky pro úpravu a odstranění.

      - Přidání dovednosti: Uživatelé mohou přidávat nové dovednosti pomocí formuláře, který obsahuje pole pro název a funkci dovednosti. 
        Po odeslání formuláře je dovednost přidána do seznamu a zobrazena na ovládacím panelu.
      
      - Editace dovednosti: Uživatelé mohou upravovat existující dovednosti kliknutím na tlačítko "Edit" vedle dovednosti. 
        Formulář pro úpravu dovednosti se zobrazí, předvyplněný s daty dovednosti. Uživatel může aktualizovat název nebo funkci dovednosti a potvrdit změny.
        
      - Odebrání dovednosti: Uživatelé mohou odstranit dovednost ze seznamu kliknutím na tlačítko "Remove" vedle dovednosti.
      
      - Odhlášení: Uživatelé se mohou odhlásit z aplikace kliknutím na tlačítko "Logout". Po odhlášení jsou uživatelé přesměrováni na stránku pro přihlášení.
   
![Dashboard image](https://github.com/Sw4tCZ/RegisterApi-SQL/blob/main/API4.png)
     
Tato aplikace je rozdělena na části: 

- Frontend: Aplikace má HTML, CSS a JavaScript pro prezentaci a interakci s uživatelem. JavaScript je použit pro manipulaci s DOM a komunikaci s backendem prostřednictvím AJAX požadavků.

- Backend: Aplikace má backend část postavenou na frameworku Flask. Flask je zodpovědný za zpracování HTTP požadavků, autentizaci uživatelů a komunikaci s databází pro ukládání a načítání dovedností uživatelů. Backend také poskytuje API pro manipulaci s dovednostmi a autentizaci uživatelů.

- Databáze: Aplikace používá databázi pro ukládání a načítání informací o uživatelích a jejich dovednostech. 

- Autentizace: Aplikace používá JWT tokeny pro autentizaci uživatelů. Po úspěšném přihlášení se uživateli přidělí přístupový token, který je poté použit pro ověřování uživatelových požadavků na backend.

![Dashboard image](https://github.com/Sw4tCZ/RegisterApi-SQL/blob/main/API5.png)






