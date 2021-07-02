import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';

import { AppComponent } from './app.component';
import { ComicComponent } from './comic/comic.component';
import { ComicService } from './comic.service';


@NgModule({
  declarations: [
    AppComponent,
    ComicComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
  ],
  providers: [ComicService],
  bootstrap: [AppComponent]
})
export class AppModule { }
