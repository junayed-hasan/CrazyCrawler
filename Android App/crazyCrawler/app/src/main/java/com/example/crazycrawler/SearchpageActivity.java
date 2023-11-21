package com.example.crazycrawler;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.net.Uri;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonArrayRequest;
import com.android.volley.toolbox.Volley;
import com.bumptech.glide.Glide;
import com.google.android.gms.auth.api.signin.GoogleSignIn;
import com.google.android.gms.auth.api.signin.GoogleSignInAccount;
import com.google.android.gms.auth.api.signin.GoogleSignInClient;
import com.google.android.gms.auth.api.signin.GoogleSignInOptions;
import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;

import org.json.JSONArray;
import org.json.JSONException;

import java.util.ArrayList;

public class SearchpageActivity extends AppCompatActivity {
    Button signout;
    GoogleSignInClient mGoogleSignInClient;
    TextView username, email;
    ImageView photo;

    ArrayList<Object> listdata = new ArrayList<Object>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_searchpage);

        work();

        username=findViewById(R.id.username);
        email=findViewById(R.id.email);
        photo=findViewById(R.id.photo);
        signout=findViewById(R.id.signOut);

        GoogleSignInOptions gso = new GoogleSignInOptions.Builder(GoogleSignInOptions.DEFAULT_SIGN_IN)
                .requestEmail()
                .build();

        mGoogleSignInClient = GoogleSignIn.getClient(this, gso);

        signout.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                signOut();
            }
        });

        GoogleSignInAccount acct = GoogleSignIn.getLastSignedInAccount(this);

        if(acct != null)
        {
            String name = acct.getDisplayName();
            String mail = acct.getEmail();
            Uri pic = acct.getPhotoUrl();

            username.setText(name);
            email.setText(mail);
            Glide.with(this).load(String.valueOf(pic)).into(photo);
        }
    }

    private void signOut() {
        mGoogleSignInClient.signOut()
                .addOnCompleteListener(this, new OnCompleteListener<Void>() {
                    @Override
                    public void onComplete(@NonNull Task<Void> task) {
                        Toast.makeText(SearchpageActivity.this, "signout", Toast.LENGTH_SHORT).show();
                        finish();
                    }
                });
    }

    private void work(){

        String URL = "http://10.0.2.2:8000/api/users/";

        RequestQueue requestQueue = Volley.newRequestQueue(this);

        JsonArrayRequest objectRequest = new JsonArrayRequest(
                URL,
                new Response.Listener<JSONArray>() {
                    @Override
                    public void onResponse(JSONArray jsonArray) {
                        for (int i=0;i<jsonArray.length();i++){

                            //Adding each element of JSON array into ArrayList
                            try {
                                listdata.add(jsonArray.get(i));
                            } catch (JSONException e) {
                                e.printStackTrace();
                            }
                        }

                        System.out.println("Each element of ArrayList");
                        for(int i=0; i<listdata.size(); i++) {
                            //Printing each element of ArrayList
                            System.out.println(listdata.get(i));
                        }
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Log.e("JSON error",error.toString());
                    }
                }
        );

        requestQueue.add(objectRequest);
    }
}