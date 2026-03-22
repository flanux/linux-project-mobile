# Add project specific ProGuard rules here.
-keepattributes *Annotation*, InnerClasses
-dontnote kotlinx.serialization.AnnotationsKt

-keepclassmembers class kotlinx.serialization.json.** {
    *** Companion;
}
-keepclasseswithmembers class kotlinx.serialization.json.** {
    kotlinx.serialization.KSerializer serializer(...);
}

-keep,includedescriptorclasses class com.linuxproject.**$$serializer { *; }
-keepclassmembers class com.linuxproject.** {
    *** Companion;
}
-keepclasseswithmembers class com.linuxproject.** {
    kotlinx.serialization.KSerializer serializer(...);
}
